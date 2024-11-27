document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone');
    const form = document.getElementById('frmMain');

    // Formatação do telefone
    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, ''); // Remove tudo que não for número

        if (value.length > 0) {
            if (value.length <= 2) {
                value = `(${value}`; // Formato (XX
            } else if (value.length <= 7) {
                value = `(${value.substring(0, 2)}) ${value.substring(2)}`; // Formato (XX) XXXXX
            } else {
                value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7, 11)}`; // Formato (XX) XXXXX-XXXX
            }
        }

        e.target.value = value; // Atualiza o campo com o valor formatado
    });

    // Validação ao sair do campo (blur)
    phoneInput.addEventListener('blur', function(e) {
        const value = e.target.value.replace(/\D/g, ''); // Remove tudo que não for número
        if (value.length < 10 || value.length > 11) {
            alert('Por favor, insira um número válido com DDD e telefone completo.');
            e.target.value = ''; // Limpa o campo se o número não for válido
        }
    });

    // Evento de envio do formulário
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        let formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            description: document.getElementById('description').value
        };

        // Envia a requisição para o servidor
        fetch('/api/cotacao', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Exibe a modal de sucesso
                showModal(data.message);

                // Limpar os campos do formulário após envio
                form.reset(); // Limpa todos os campos do formulário
            } else if (data.error) {
                alert('Erro: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Houve um erro ao enviar o orçamento. Tente novamente.');
        });
    });

    // Função para exibir a modal
    function showModal(message) {
        const modal = document.getElementById('successModal');
        const modalContent = modal.querySelector('.modal-content p');
        modalContent.textContent = message; // Altera o texto da mensagem na modal

        modal.style.display = 'flex'; // Exibe a modal com display flex

        // Fecha a modal quando o usuário clicar no "X"
        const closeButton = modal.querySelector('.close');
        closeButton.onclick = function() {
            modal.style.display = 'none';
        };

        // Fecha a modal quando clicar fora da caixa de conteúdo
        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };

        // Fechar a modal após 5 segundos automaticamente (opcional)
        setTimeout(function() {
            modal.style.display = 'none';
        }, 5000);
    }

    // Remover parâmetros e hash da URL ao carregar a página
    window.onload = function() {
        const currentUrl = window.location.href;
        const baseUrl = window.location.origin + window.location.pathname;

        if (currentUrl !== baseUrl) {
            // Atualiza a URL sem recarregar a página
            window.history.replaceState({}, document.title, baseUrl);
        }
    };

    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const socialBar = document.querySelector('.social-bar');
        if (window.scrollY > lastScrollY) {
            socialBar.classList.add('hidden'); // Esconde ao rolar para baixo
        } else {
            socialBar.classList.remove('hidden'); // Mostra ao rolar para cima
        }
        lastScrollY = window.scrollY;
    });
});
