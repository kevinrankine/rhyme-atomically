require 'hdf5'
require 'nn'
require 'rnn'
require 'optim'
require 'cutorch'
require 'cunn'

cmd = torch.CmdLine()
cmd:option('-datafile', './data/data.hdf5', 'data file')

function main()
   opt = cmd:parse(arg)
   local datafile = hdf5.open(opt.datafile, 'r')

   local X = datafile:read("X"):all():long()
   local y = datafile:read("y"):all():long()
   local word_vectors = datafile:read("word_vectors"):all():float()

   neural_network(X, y, word_vectors)
end

function neural_network(X, y, word_vectors)
   local bsize = 8
   local lsize = 50
   local eta = 1e-1


   local nwords = word_vectors:size(1)
   local d_in = word_vectors:size(2)
   local d_hid = 400
   
   local model = nn.Sequential()
   
   local LT = nn.LookupTable(nwords, d_in)
   LT.weight:copy(word_vectors)

   model:add(LT)
   model:add(nn.SplitTable(2))
   model:add(nn.Sequencer(nn.FastLSTM(d_in, d_hid, lsize)))
   model:add(nn.Sequencer(nn.Linear(d_hid, nwords)))
   model:add(nn.Sequencer(nn.LogSoftMax()))

   criterion = nn.SequencerCriterion(nn.ClassNLLCriterion())

   model:cuda()
   criterion:cuda()

   model:remember('neither')

   params, gradParams = model:getParameters()

   for ii = 1, X:size(1), 0 do
      gradParams:zero()
      
      print (ii)
      xx = X:narrow(1, ii, bsize):cuda()
      yy = y:narrow(1, ii, bsize):split(1, 2)

      yy = map(function(x) return x:select(2, 1):cuda() end, yy)
      local out = model:forward(xx)

      local loss = criterion:forward(out, yy)
      local grad = criterion:backward(out, yy)

      model:backward(xx, grad)
      renorm_grad(5, gradParams)
      model:updateParameters(eta)

      print (loss)
   end
end

function map(func, array)
   local new_array = {}
   
   for i,v in ipairs(array) do
      new_array[i] = func(v)
   end
   
   return new_array
end

function renorm_grad(thresh, gradParams)
   local norm = gradParams:norm()

   if (norm > thresh) then
      gradParams:div(norm / thresh)
   end
   
end

main()

