checkin
=======

1.Introduction
===============================================================
Checkin for every single website that you have interested with.

2.About Configure File
===============================================================
You need a configure named 'checkin.yaml' for running this scr-
ipt while its structure should be like this below.

checkin.yaml
---------------------------------------------------------------
version 1:
    website:
	<your_interest_website1>:
	    [your_named_label]:
		username:[your_accout1_username]
		password:[your_accout1_password]
	    [your_named_label_2]:
		username:[your_accout2_username]
		password:[your_accout2_password]
	<your_interest_other_website>:
	    [your_named_label]:
		username:[your_accout_username]
		password:[your_accout_password]
----------------------------------------------------------------

Note:
    Support website(you can replace content in angle bracket):
	taobao(www.taobao.com)

3.How To Run It
================================================================
Well, It's easy.

[you@yourhost ~]#./main.py start

It should run in daemon mode.But if you don't like daemon mode,
this command should be fit for you.

[you@yourhost ~]#./main.py nodaemon


