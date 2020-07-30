import compactor
import drive
import sys

def show_upload_options(itens):
    allowed_itens = []
    for item in itens:
        if len(item.split('.')) == 1:
            allowed_itens.append(item)
    if len(allowed_itens) <= 0:
        sys.exit()
    print('\nDo you want to upload any folder?\n')
    print('[0] No')
    for i in range(0,len(allowed_itens)):
        print('[{}] {}'.format(i+1,allowed_itens[i]))
    print('[{}] All'.format(len(allowed_itens)+1))
    choice = input('\nOption: ')
    if choice == '0': #None
        sys.exit()
    if choice.find(',') == -1 and int(choice) == len(allowed_itens)+1: #All
        index = 1
        for folder in allowed_itens:
            path = './' + folder
            print('\n{} of {}'.format(index,len(allowed_itens)))
            print('Compressing {}'.format(folder))
            zip_file = compactor.build_zip(path)
            drive.upload(zip_file)
            index += 1
    #Custom
    choices = choice.split(',')
    index = 1
    for i in range(0,len(choices)):
        print('\n{} of {}'.format(index,len(choices)))
        path = './' + allowed_itens[int(choices[i])-1]
        print('Compressing {}'.format(allowed_itens[int(choices[i])-1]))
        zip_file = compactor.build_zip(path)
        drive.upload(zip_file)
        index += 1