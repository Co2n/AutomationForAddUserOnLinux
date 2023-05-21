import paramiko

root_uid = "root"
root_pwd = "rootpassword"
newpass_user = "P@ssw0rd1"
#read file
file1 = open('list.txt', 'r')
Lines = file1.readlines()
for line in Lines:
    host = line.strip()
    print("Host : " + host + " Porcessing ...")
try:
      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(host, username=root_uid, password=root_pwd)
      stdin, stdout, stderr = client.exec_command('ls')
      output = stdout.readlines()
      print("success authenticated")
      with open(host+".txt", "w") as f:
         for line in output:
               if line.rstrip() == "export":
                  print("creating user ..... using export directory")
                  stdin, stdout, stderr = client.exec_command('useradd user -c "User ID Manage PIM"')
                  output = stdout.readlines()
                  f.write(output + "\n")
         print("creating user ....... default directory")
         try:
              (stdin, stdout, stderr) = client.exec_command('sudo useradd user -c "User ID Manage PIM"')
              output1 = stdout.read()
            #   f.write(output1)
              print("User user created")
         except Exception as e:
              print(e)
            #   f.write(e)
         
         print("Change password user")
         try:
              (stdin, stdout, stderr) = client.exec_command('sudo passwd user')
              stdin.write(newpass_user + '\n')
              stdin.write(newpass_user + '\n')
              stdin.flush()
              output1 = stdout.readlines()
            #   f.write(output1)
              print("Password user changed")
         except Exception as e:
              print(e)
            #   f.write(e)
         
         print("VISUDO user")
         try:
            stdin, stdout, stderr = client.exec_command("cat /root/test.conf")
            all_lines = ''
            for line in stdout.readlines():
               all_lines += line
            new_line = all_lines + '\n' 
            (stdin, stdout, stderr) = client.exec_command("echo 'user  ALL=(ALL)   NOPASSWD:ALL' >> /etc/sudoers".format(new_line))
            output1 = stdout.readlines()
            # f.write(output1)
            print("VISUDO for user changed")
         except Exception as e:
              print(e)
            #   f.write(e)
         print("===============================")
         f.write(line.rstrip())
except Exception as e:
      print(e)