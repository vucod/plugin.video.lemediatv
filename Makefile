name = plugin.video.lemediatv

all: clean zip

clean:
	rm -rf ../$(name).zip 

zip: 
	zip -r ../$(name).zip  ../$(name)

