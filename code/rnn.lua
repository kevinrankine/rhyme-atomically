require 'hdf5'
require 'nn'
require 'rnn'
require 'optim'

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
    local nwords = word_vectors:size(1)
    local d_in = word_vectors:size(2)
    
    local model = nn.Sequential()
    
    local LT = nn.LookupTable(nwords, d_in)
    LT.weight:copy(word_vectors)

    model:add(LT)
    model:add(nn.SplitTable(1))
    model:add(nn.Sequencer(nn.GRU(d_in, d_in)))
    model:add(nn.Sequencer(nn.Linear(d_in, nwords)))
    model:add(nn.Sequencer(nn.LogSoftMax()))

    local out = model:forward(X[1])

end	

main()

