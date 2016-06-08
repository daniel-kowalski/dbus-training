PICS=final.png

all: $(PICS)

clean:
	rm *.png

%.png: %.ditaa $(DEPS)
	ditaa -E $< $@