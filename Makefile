# Artefacto de build. No instala y no levanta la tienda.
VERSION := 0.1.0

.PHONY: build
build:
	rm -rf dist
	mkdir -p dist
	tar -czf dist/secureshop-$(VERSION).tar.gz \
		--exclude '__pycache__' \
		-C SecureShop \
		api.py secureshop.py nucleo templates requirements.txt .env.example
	@echo "Artefacto: dist/secureshop-$(VERSION).tar.gz"
