# Tool
RSVG = rsvg-convert

# Output directory
IMGDIR = ../img

# Molecules and types
MOLECULES = ch4 co ethylene
TYPES = canonical localized

# Input SVGs
SVGS = $(foreach m,$(MOLECULES),$(foreach t,$(TYPES),mo_$(m)_$(t).svg))

# Output PNGs (same base name, different directory)
PNGS = $(patsubst %.svg,$(IMGDIR)/%.png,$(SVGS))

# Default target
all: $(IMGDIR) $(PNGS)

# Ensure output directory exists
$(IMGDIR):
	mkdir -p $(IMGDIR)

# Pattern rule: SVG -> ../img/PNG
$(IMGDIR)/%.png: %.svg | $(IMGDIR)
	$(RSVG) -f png -o $@ $<

# Clean generated images
clean:
	rm -f $(PNGS)

.PHONY: all clean
