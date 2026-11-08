# Construcción

No hay un paquete que instalar en otro lado. No hay imagen de Docker, ni wheel, ni `npm run build`. El artefacto es el árbol de fuentes más `SecureShop/requirements.txt`.

`run-local.sh` crea el entorno virtual `.venv` si no existe, instala esas dependencias y levanta los dos procesos. El `.venv` y `secure_shop.db` no se versionan. Se recrean en la máquina.

El CI de GitHub hace el mismo install y corre pytest. No publica un binario. El reporte de esa corrida, y la corrida de la noche, están en [`../operacion.md`](../operacion.md).

Las decisiones de lenguaje y de framework están en [`../05-decisiones/tecnologias.md`](../05-decisiones/tecnologias.md).
