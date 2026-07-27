/**
 * image-preview.js
 * Preview de imagens antes do upload
 * 
 * Funcionalidade:
 * - Ao selecionar imagens no input[type="file"], exibe miniaturas
 * - Suporte a múltiplas imagens
 * - Botão para remover imagem individualmente
 * - Validação de tipo (apenas imagens) e tamanho (máx 5MB)
 */

document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.querySelector('input[type="file"][name="immobile"]');
  if (!fileInput) return;

  // Cria container de preview após o input
  const previewContainer = document.createElement('div');
  previewContainer.id = 'image-preview-container';
  previewContainer.className = 'row g-2 mt-2';
  fileInput.parentElement.appendChild(previewContainer);

  // Array para armazenar os arquivos selecionados
  let selectedFiles = [];

  fileInput.addEventListener('change', function (e) {
    const files = Array.from(e.target.files);
    const validFiles = [];
    const errors = [];

    for (const file of files) {
      // Valida tipo
      if (!file.type.startsWith('image/')) {
        errors.push(`"${file.name}" não é uma imagem.`);
        continue;
      }

      // Valida tamanho (5MB)
      if (file.size > 5 * 1024 * 1024) {
        errors.push(`"${file.name}" excede 5MB.`);
        continue;
      }

      // Verifica se já não foi adicionado (pelo nome)
      const alreadyAdded = selectedFiles.some(
        (f) => f.name === file.name && f.size === file.size
      );
      if (!alreadyAdded) {
        validFiles.push(file);
      }
    }

    if (errors.length > 0) {
      showFileErrors(errors);
    }

    // Adiciona os arquivos válidos à lista
    selectedFiles = selectedFiles.concat(validFiles);

    // Recria o FileList no input para enviar corretamente
    updateFileInput(fileInput, selectedFiles);

    // Renderiza os previews
    renderPreviews(selectedFiles, previewContainer);
  });

  /**
   * Exibe erros de validação de arquivo
   */
  function showFileErrors(errors) {
    // Remove mensagem de erro anterior se existir
    const oldAlert = document.getElementById('image-preview-error');
    if (oldAlert) oldAlert.remove();

    const alertDiv = document.createElement('div');
    alertDiv.id = 'image-preview-error';
    alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-2 py-2';
    alertDiv.innerHTML = `
      <strong>Erro ao selecionar imagem(ns):</strong>
      <ul class="mb-0 mt-1">
        ${errors.map((e) => `<li>${e}</li>`).join('')}
      </ul>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    `;
    fileInput.parentElement.appendChild(alertDiv);
  }

  /**
   * Renderiza os previews das imagens
   */
  function renderPreviews(files, container) {
    container.innerHTML = '';

    if (files.length === 0) return;

    files.forEach(function (file, index) {
      const reader = new FileReader();

      const col = document.createElement('div');
      col.className = 'col-4 col-md-3';

      const card = document.createElement('div');
      card.className = 'card image-preview-card';
      card.style.cssText = 'border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden;';

      const imgWrapper = document.createElement('div');
      imgWrapper.style.cssText = 'position: relative; width: 100%; padding-top: 75%; overflow: hidden; background: #f8f9fa;';

      const img = document.createElement('img');
      img.style.cssText =
        'position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;';

      const deleteBtn = document.createElement('button');
      deleteBtn.type = 'button';
      deleteBtn.className = 'btn btn-sm btn-danger';
      deleteBtn.style.cssText =
        'position: absolute; top: 4px; right: 4px; border-radius: 50%; width: 24px; height: 24px; padding: 0; display: flex; align-items: center; justify-content: center; font-size: 12px; line-height: 1;';
      deleteBtn.innerHTML = '&times;';
      deleteBtn.title = 'Remover imagem';
      deleteBtn.addEventListener('click', function (e) {
        e.preventDefault();
        // Remove o arquivo do array
        selectedFiles.splice(index, 1);
        // Atualiza o input e re-renderiza
        updateFileInput(fileInput, selectedFiles);
        renderPreviews(selectedFiles, container);
      });

      const cardBody = document.createElement('div');
      cardBody.className = 'card-body p-1 text-center';
      cardBody.style.cssText = 'font-size: 11px;';

      const fileName = document.createElement('small');
      fileName.className = 'text-muted text-truncate d-block';
      fileName.textContent = file.name.length > 18
        ? file.name.substring(0, 15) + '...'
        : file.name;

      const fileSize = document.createElement('small');
      fileSize.className = 'text-muted d-block';
      fileSize.textContent = formatFileSize(file.size);

      reader.onload = function (e) {
        img.src = e.target.result;
        img.alt = file.name;
      };
      reader.readAsDataURL(file);

      imgWrapper.appendChild(img);
      imgWrapper.appendChild(deleteBtn);
      card.appendChild(imgWrapper);
      cardBody.appendChild(fileName);
      cardBody.appendChild(fileSize);
      card.appendChild(cardBody);
      col.appendChild(card);
      container.appendChild(col);
    });
  }

  /**
   * Atualiza o FileList do input com os arquivos selecionados
   */
  function updateFileInput(input, files) {
    // Cria um novo DataTransfer e adiciona os arquivos
    const dataTransfer = new DataTransfer();
    files.forEach(function (file) {
      dataTransfer.items.add(file);
    });
    input.files = dataTransfer.files;
  }

  /**
   * Formata tamanho do arquivo
   */
  function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }
});

