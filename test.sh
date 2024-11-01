./vast create instance 13444221  --image  jjziets/vasttest:latest  --ssh --direct --env '-e TZ=PDT -e XNAME=XX4 -p 5000:5000' --disk 20 --onstart-cmd 'python3 remote.py'
