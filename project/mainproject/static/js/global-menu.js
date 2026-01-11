const togglerButton = document.querySelector(".navbar-toggler");
const togglerTarget = document.querySelector(".collapse");
const currentUrl = window.location.href;

// /accounts/ではヘッダーの要素をフッターに表示するため、ボタンは非表示
if (currentUrl.includes("/accounts/")){
    togglerButton.classList.add("accounts-page");
}