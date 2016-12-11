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

   local perm = torch.randperm(X:size(1)):long()
   X = X:index(1, perm)
   y = y:index(1, perm)

   -- train_X = X:narrow(1, 1, 350)
   -- train_y = y:narrow(1, 1, 350)

   -- test_X = X:narrow(1, 350, 68)
   -- test_y = y:narrow(1, 350, 68)

   train_X = X
   train_y = y

   neural_network(train_X, train_y, word_vectors)
end

function neural_network(X, y, word_vectors)
   y = X -- IMPORTANT REMOVE THIS
   local bsize = 8
   local lsize = 50
   local eta = 1e-2

   local nwords = word_vectors:size(1)
   local d_in = word_vectors:size(2)
   local d_hid = 400
   
   local model = nn.Sequential()
   
   local LT = nn.LookupTable(nwords, d_in)
   LT.weight:copy(word_vectors)

   model:add(LT)
   model:add(nn.SplitTable(2))
   model:add(nn.Sequencer(nn.FastLSTM(d_in, d_hid)))
   model:add(nn.Sequencer(nn.Linear(d_hid, nwords)))
   model:add(nn.Sequencer(nn.LogSoftMax()))

   local criterion = nn.SequencerCriterion(nn.ClassNLLCriterion(), true)

   model:cuda()
   criterion:cuda()

   model:remember('both')

   params, gradParams = model:getParameters()
   for epoch = 1, 25 do
      local total_loss = 0

      for ii = 1, X:size(1) - bsize, bsize do
	 for jj = 1, X:size(2), lsize do
	    gradParams:zero()
	    
	    local xx = X:narrow(1, ii, bsize):narrow(2, jj, lsize):cuda()
	    local yy = y:narrow(1, ii, bsize):narrow(2, jj, lsize):split(1, 2)

	    yy = map(function(x) return x:select(2, 1):cuda() end, yy)
	    local out = model:forward(xx)

	    local loss = criterion:forward(out, yy)
	    local grad = criterion:backward(out, yy)

	    model:backward(xx, grad)
	    renorm_grad(10, gradParams)
	    
	    model:updateParameters(eta)
	    model:forget()

	    total_loss = total_loss + loss
	 end
	 
	 print (string.format("%.1f%%", 100 * ii / X:size(1)))
      end

      print (string.format("Total loss after %d epochs: %.3f", epoch, total_loss / ((X:size(1) / bsize) * (X:size(2) / lsize))))
   end
end

function validate(model, X_valid, y_valid)
   local criterion = nn.SequencerCriterion(nn.ClassNLLCriterion())
   for ii = 1, X_valid:size(1) do
      
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

