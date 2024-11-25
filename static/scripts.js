document.getElementById('frmMain').addEventListener('submit', function(event) {
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
            document.getElementById('frmMain').reset(); // Limpa todos os campos do formulário
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

    modal.style.display = 'block'; // Exibe a modal

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
}

document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone');

    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, ''); // Remove tudo que não for número

        // Aplica a formatação (XX) XXXXX-XXXX
        if (value.length > 0) {
            if (value.length <= 2) {
                value = `(${value}`;
            } else if (value.length <= 7) {
                value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
            } else {
                value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7, 11)}`;
            }
        }

        e.target.value = value; // Atualiza o campo com o valor formatado
    });

    phoneInput.addEventListener('blur', function(e) {
        // Valida o tamanho do número ao sair do campo
        const value = e.target.value.replace(/\D/g, ''); // Remove tudo que não for número
        if (value.length < 10 || value.length > 11) {
            alert('Por favor, insira um número válido com DDD e telefone completo.');
            e.target.value = ''; // Limpa o campo se o número não for válido
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const prevButton = document.querySelector('.control-prev');
    const nextButton = document.querySelector('.control-next');
    const slider = document.querySelector('.slider');
    let currentIndex = 0;
    const slideCount = slides.length;

    function updateCarousel() {
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;
        dots.forEach(dot => dot.classList.remove('selected'));
        dots[currentIndex].classList.add('selected');
    }

    function goToNextSlide() {
        currentIndex = (currentIndex + 1) % slideCount;
        updateCarousel();
    }

    function goToPrevSlide() {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateCarousel();
    }

    dots.forEach(dot => {
        dot.addEventListener('click', function () {
            currentIndex = parseInt(this.getAttribute('data-index'));
            updateCarousel();
        });
    });

    nextButton.addEventListener('click', goToNextSlide);
    prevButton.addEventListener('click', goToPrevSlide);

    setInterval(goToNextSlide, 5000); // Desliza automaticamente a cada 5 segundos
});

// Remover parâmetros e hash da URL ao carregar a página
window.onload = function () {
    const currentUrl = window.location.href;
    const baseUrl = window.location.origin + window.location.pathname;
    
    if (currentUrl !== baseUrl) {
        // Atualiza a URL sem recarregar a página
        window.history.replaceState({}, document.title, baseUrl);
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navbar = document.querySelector(".navbar");

    menuToggle.addEventListener("click", function () {
        navbar.classList.toggle("active");
    });
});

