import compactor
import drive
import sys

def show_upload_options(itens):
    print('\nDo you want to upload a folder?\n')
    print('[0] No')
    allowed_itens = []
    for item in itens:
        if len(item.split('.')) == 1:
            allowed_itens.append(item)
    for i in range(0,len(allowed_itens)):
        print('[{}] {}'.format(i+1,allowed_itens[i]))
    print('[{}] All'.format(len(allowed_itens)+1))
    choice = int(input('\nOption: '))
    if choice == 0: #None
        sys.exit()
    if choice == len(allowed_itens)+1: #All
        index = 1
        for folder in allowed_itens:
            path = './' + folder
            print('\n{} of {}'.format(index,len(allowed_itens)))
            print('Compressing {}'.format(folder))
            zip_file = compactor.build_zip(path)
            drive.upload(zip_file)
            index += 1
    if choice > 0 and choice < len(allowed_itens)+1: #Single
        path = './' + allowed_itens[choice-1]
        print('\nCompressing {}'.format(allowed_itens[choice-1]))
        zip_file = compactor.build_zip(path)
        drive.upload(zip_file)