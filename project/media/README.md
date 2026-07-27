# media/

Diretório de arquivos enviados pelos usuários (uploads).

## Configuração

As configurações relacionadas ao diretório `media/` estão em `project/proj/settings.py`:

```python
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')   # Caminho absoluto no disco
MEDIA_URL = '/media/'                          # URL pública para acessar os arquivos
```

- **MEDIA_ROOT**: Define o caminho físico no servidor onde os arquivos são armazenados (`project/media/`)
- **MEDIA_URL**: Define a URL base para acessar os arquivos via navegador (`http://127.0.0.1:8000/media/...`)

As rotas para servir arquivos de mídia em desenvolvimento são configuradas em `project/proj/urls.py`:

```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Como funciona

1. O modelo `ImmobileImage` salva as imagens em `media/images/`
2. O template `list_location.html` exibe as imagens via `{{ el.image.url }}`
3. Em desenvolvimento, o Django serve os arquivos em `/media/`
