# Checkin

## Introduction
Checkin for every single website that you have interested with.

## About Configure File
You need a configure named __'checkin.yaml'__ for running this script while its structure should be like this below.

```yaml
version 1:
immediately: false # When this script startup, checkin immediately or not.
taobao:
    chktime: 08:22-09:20 # The website should be checkin in this period.
    account:
	- username:[your_accout1_username]
	  password:[your_accout1_password]
	    
	- username:[your_accout_username]
	  password:[your_accout_password]
```

Note: Support website(you can replace content in angle brackets):
- [taobao](http://www.taobao.com "taobao")
- [etao](http://www.etao.com "etao")

## How To Run It

Well, It's easy.
```python
[you@yourhost ~]#./main.py start
```

It should run in daemon mode.But if you don't like daemon mode,
this command should be fit for you.
```python
[you@yourhost ~]#./main.py nodaemon
```

## Contributing
1. Fork it.
2. Create a branch (`git checkout -b my_checkin`)
3. Commit your changes (`git commit -am "feature some interesting"`)
4. Push to the branch (`git push origin my_checkin`)
5. Open a [Pull Request][1]
6. Enjoy something else and wait

[1]: http://github.com/tinyboyz/checkin/pulls
