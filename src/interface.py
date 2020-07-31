import compactor
import drive
import sys

def show_upload_options(itens):
    print('\nDo you want to upload any item?\n')
    print('[0] No')
    for i in range(0,len(itens)):
        print('[{}] {}'.format(i+1,itens[i]))
    print('[{}] All'.format(len(itens)+1))
    choice = input('\nOption: ')
    if choice == '0': #None
        sys.exit()
    if choice.find(',') == -1 and int(choice) == len(itens)+1: #All
        index = 1
        for item in itens:
            print('\n{} of {}'.format(index,len(itens)))
            if item.find('.') != -1: #is file
                drive.upload(item)
            else: #is folder
                path = './' + item          
                print('Compressing {}'.format(item))
                zip_file = compactor.build_zip(path)
                drive.upload(zip_file, True)
            index += 1
        sys.exit()
    #Custom
    choices = choice.split(',')
    index = 1
    for i in range(0,len(choices)):
        print('\n{} of {}'.format(index,len(choices)))
        if itens[int(choices[i])-1].find('.') != -1: #is file
            drive.upload(itens[int(choices[i])-1])
        else:
            path = './' + itens[int(choices[i])-1]
            print('Compressing {}'.format(itens[int(choices[i])-1]))
            zip_file = compactor.build_zip(path)
            drive.upload(zip_file, True)
        index += 1
    sys.exit()