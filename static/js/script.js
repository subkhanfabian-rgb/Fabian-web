const hamburger = document.getElementById("hamburger");
const navMenu = document.getElementById("navMenu");
const navLinks = document.querySelectorAll(".nav-menu a");
const navbar = document.querySelector(".navbar");
const themeToggle = document.getElementById("themeToggle");
const themeIcon = themeToggle.querySelector("i");
const contactForm = document.getElementById("contactForm");
const formMessage = document.getElementById("formMessage");
const currentYear = document.getElementById("currentYear");

/* Tahun footer otomatis */
currentYear.textContent = new Date().getFullYear();

/* Menu mobile */
hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
});

navLinks.forEach((link) => {
    link.addEventListener("click", () => {
        hamburger.classList.remove("active");
        navMenu.classList.remove("active");
    });
});

/* Navbar saat scroll */
window.addEventListener("scroll", () => {
    navbar.classList.toggle("scrolled", window.scrollY > 20);
});

/* Tema terang dan gelap */
const savedTheme = localStorage.getItem("portfolio-theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    themeIcon.classList.replace("fa-moon", "fa-sun");
}

themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    const isDarkMode = document.body.classList.contains("dark-mode");

    if (isDarkMode) {
        themeIcon.classList.replace("fa-moon", "fa-sun");
        localStorage.setItem("portfolio-theme", "dark");
    } else {
        themeIcon.classList.replace("fa-sun", "fa-moon");
        localStorage.setItem("portfolio-theme", "light");
    }
});

/* Animasi elemen ketika muncul */
const revealElements = document.querySelectorAll(".reveal");

const revealObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");

                const progressBars = entry.target.querySelectorAll(".progress-fill");

                progressBars.forEach((bar) => {
                    bar.style.width = `${bar.dataset.progress}%`;
                });

                revealObserver.unobserve(entry.target);
            }
        });
    },
    {
        threshold: 0.15
    }
);

revealElements.forEach((element) => {
    revealObserver.observe(element);
});

/* Nav link aktif sesuai section */
const sections = document.querySelectorAll("main section");

const sectionObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                navLinks.forEach((link) => {
                    link.classList.remove("active");

                    if (link.getAttribute("href") === `#${entry.target.id}`) {
                        link.classList.add("active");
                    }
                });
            }
        });
    },
    {
        threshold: 0.45
    }
);

sections.forEach((section) => {
    sectionObserver.observe(section);
});

/* Kirim form ke Flask */
contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitButton = contactForm.querySelector("button[type='submit']");
    const formData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value
    };

    submitButton.disabled = true;
    submitButton.innerHTML = `
        Mengirim...
        <i class="fa-solid fa-spinner fa-spin"></i>
    `;

    formMessage.textContent = "";
    formMessage.className = "form-message";

    try {
        const response = await fetch("/contact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            formMessage.textContent = result.message;
            formMessage.classList.add("success");
            contactForm.reset();
        } else {
            formMessage.textContent = result.message || "Pesan gagal dikirim.";
            formMessage.classList.add("error");
        }
    } catch (error) {
        formMessage.textContent = "Terjadi kesalahan. Pastikan server Flask berjalan.";
        formMessage.classList.add("error");
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = `
            Kirim Pesan
            <i class="fa-solid fa-paper-plane"></i>
        `;
    }
});