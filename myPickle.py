import cPickle as Pickle

def save(obj, fo_path):
    fo_pkl = file(fo_path, 'wb')
    Pickle.dump(obj, fo_pkl, True)
    print 'Pickle %s saved!' % fo_path

def load(fi_path):
    fi_pkl = file(fi_path, 'rb')
    return Pickle.load(fi_pkl)
