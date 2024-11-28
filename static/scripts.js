document.addEventListener('DOMContentLoaded', function () {
    const phoneInput = document.getElementById('phone');
    const form = document.getElementById('frmMain');

    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length > 0) {
                if (value.length <= 2) {
                    value = `(${value}`;
                } else if (value.length <= 7) {
                    value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
                } else {
                    value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7, 11)}`;
                }
            }

            e.target.value = value;
        });

        phoneInput.addEventListener('blur', function (e) {
            const value = e.target.value.replace(/\D/g, '');
            if (value.length < 10 || value.length > 11) {
                alert('Por favor, insira um número válido com DDD e telefone completo.');
                e.target.value = '';
            }
        });
    } else {
        console.error("Campo de telefone não encontrado. Verifique o ID do campo.");
    }

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário

            const phoneValue = phoneInput.value.replace(/\D/g, '');
            if (phoneValue.length < 10 || phoneValue.length > 11) {
                alert('Número de telefone inválido!');
                return;
            }

            let formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: phoneInput.value,
                description: document.getElementById('description').value
            };

            // Envia os dados via fetch
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
                    showModal(data.message); // Exibe o modal com a mensagem de sucesso

                    form.reset(); // Reseta o formulário após sucesso
                } else if (data.error) {
                    alert('Erro: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Houve um erro ao enviar o orçamento. Tente novamente.');
            });
        });
    } else {
        console.error("Formulário não encontrado. Verifique o ID do formulário.");
    }

    function showModal(message) {
        const modal = document.getElementById('successModal');
        const modalContent = modal.querySelector('.modal-content p');
        modalContent.textContent = message;

        modal.style.display = 'flex';

        const closeButton = modal.querySelector('.close');
        closeButton.onclick = function() {
            modal.style.display = 'none';
        };

        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };

        setTimeout(function() {
            modal.style.display = 'none';
        }, 5000);
    }

    window.onload = function() {
        const currentUrl = window.location.href;
        const baseUrl = window.location.origin + window.location.pathname;

        if (currentUrl !== baseUrl) {
            window.history.replaceState({}, document.title, baseUrl);
        }
    };

    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const socialBar = document.querySelector('.social-bar');
        if (window.scrollY > lastScrollY) {
            socialBar.classList.add('hidden');
        } else {
            socialBar.classList.remove('hidden');
        }
        lastScrollY = window.scrollY;
    });
});

// Função para atualizar a cor do campo com base no valor selecionado
function atualizarCorStatus(selectElement) {
    // Obtém o valor atual do campo
    const valor = parseInt(selectElement.value);

    // Remove todas as classes de cor previamente adicionadas
    selectElement.classList.remove('status-vermelho', 'status-azul', 'status-verde');

    // Aplica a cor com base no valor
    if (valor === 0) {
        selectElement.classList.add('status-vermelho'); // Ainda não trabalhado
    } else if (valor === 7 || valor === 8 || valor === 9) {
        selectElement.classList.add('status-verde'); // Finalizado
    } else {
        selectElement.classList.add('status-azul'); // Em progresso
    }
}

// Evento para resetar a cor ao abrir o campo de seleção
function resetarCorStatus(selectElement) {
    selectElement.classList.remove('status-vermelho', 'status-azul', 'status-verde');
}

// Evento para definir a cor ao fechar o campo de seleção
function aplicarCorStatus(selectElement) {
    atualizarCorStatus(selectElement);
}

// Executa ao carregar a página para definir a cor inicial
document.addEventListener("DOMContentLoaded", function() {
    const statusSelect = document.getElementById('campo_status');

    // Define a cor inicial ao carregar a página
    atualizarCorStatus(statusSelect);

    // Adiciona evento de clique para resetar a cor quando o campo de seleção for aberto
    statusSelect.addEventListener('click', function() {
        resetarCorStatus(statusSelect); // Resetar a cor sempre que o campo for clicado
    });

    // Aplica a cor correta ao sair do campo de seleção (quando o campo perde o foco)
    statusSelect.addEventListener('blur', function() {
        aplicarCorStatus(statusSelect);
    });

    // Atualiza a cor ao selecionar uma nova opção (logo após a seleção, não apenas no blur)
    statusSelect.addEventListener('change', function() {
        atualizarCorStatus(statusSelect); // Atualiza a cor imediatamente após a mudança de valor
    });
});

document.getElementById('form-edicao').addEventListener('submit', function(event) {
    event.preventDefault();

    showModal("Alterado com sucesso!"); // Exibe o modal de sucesso ao submeter
});
