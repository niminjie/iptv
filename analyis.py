import sys

def main():
    class_list = []
    content_list = []
    user_list = []
    for line in open(sys.argv[1], 'r'):
        class_name = line.split(',')[2]
        user_id = line.split(',')[6].strip()
        content = line.split(',')[1]
        
        if class_name not in class_list:
            class_list.append(class_name)

        if content not in content_list:
            content_list.append(content)

        if user_id not in user_list:
            user_list.append(user_id)

    print 'User len', len(user_list)
    print 'Content len', len(content_list)
    print 'Class len', len(class_list)
if __name__ == '__main__':
   main() 
