PICS=service_full.png bus_clients.png daemon_with_clients.png

all: presentation.tex $(PICS)
	pdflatex presentation.tex
	# and second time for "tableofcontents"
	pdflatex presentation.tex

%.png: %.ditaa
	ditaa -E $< $@

clean:
	rm -f *.png
	find . -iname 'presentation.*' -and -not -iname 'presentation.tex' -delete