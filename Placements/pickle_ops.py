# pickle operation functions

import pickle


def store_in_pickle(object,picklefile_obj):
    pickle.dump(object,picklefile_obj)


def pickle_print_all(picklefile_obj):
    
    while True :
    
        try :
            obj = pickle.load(picklefile_obj)
            print(obj.get_all())

        except EOFError:
            break

