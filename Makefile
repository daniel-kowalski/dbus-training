PICS=service_full.png bus_clients.png daemon_with_clients.png

all: $(PICS)

clean:
	rm *.png

%.png: %.ditaa $(DEPS)
	ditaa -E $< $@

