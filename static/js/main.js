/* SCHOOL LANDING main.js v3 */

var pb = document.getElementById('progress-bar')
var btt = document.getElementById('btt')
var nav = document.getElementById('mainNav')

function updateScroll() {
	var st = window.pageYOffset || document.documentElement.scrollTop
	var dh = document.documentElement.scrollHeight
	var wh = window.innerHeight
	var sc = dh - wh
	if (pb) pb.style.width = sc > 0 ? (st / sc) * 100 + '%' : '0%'
	if (btt) btt.classList.toggle('visible', st > 400)
	if (nav) nav.classList.toggle('scrolled', st > 60)
}
window.addEventListener('scroll', updateScroll, { passive: true })
window.addEventListener('resize', updateScroll, { passive: true })
window.addEventListener('load', updateScroll)

if (btt)
	btt.onclick = function () {
		window.scrollTo({ top: 0, behavior: 'smooth' })
	}

/* Mobile menu */
var toggle = document.getElementById('navToggle')
var menu = document.getElementById('mobileMenu')
var mOpen = false
if (toggle) {
	toggle.onclick = function () {
		mOpen = !mOpen
		menu.style.display = mOpen ? 'block' : 'none'
		toggle.querySelector('i').className = mOpen
			? 'bi bi-x-lg fs-4 text-dark'
			: 'bi bi-list fs-4 text-dark'
	}
}
document.querySelectorAll('.mobile-nav-link').forEach(function (l) {
	l.onclick = function () {
		menu.style.display = 'none'
		mOpen = false
		if (toggle)
			toggle.querySelector('i').className = 'bi bi-list fs-4 text-dark'
	}
})

/* Programs filter */
document.querySelectorAll('.filter-btn-custom').forEach(function (btn) {
	btn.addEventListener('click', function () {
		document.querySelectorAll('.filter-btn-custom').forEach(function (b) {
			b.classList.remove('active')
		})
		btn.classList.add('active')
		var f = btn.getAttribute('data-filter')
		document.querySelectorAll('[data-category]').forEach(function (c) {
			c.style.display =
				f === 'all' || c.getAttribute('data-category') === f ? '' : 'none'
		})
	})
})

/* Counter */
function animateCounter(el) {
	var tgt = parseInt(el.getAttribute('data-counter'), 10)
	var suf = el.getAttribute('data-suffix') || ''
	var dur = 1200,
		t0 = null
	;(function step(ts) {
		if (!t0) t0 = ts
		var p = Math.min((ts - t0) / dur, 1)
		el.textContent = Math.floor((1 - Math.pow(1 - p, 3)) * tgt) + suf
		if (p < 1) requestAnimationFrame(step)
	})(performance.now())
}

/* Scroll reveal */
var io = new IntersectionObserver(
	function (entries) {
		entries.forEach(function (e) {
			if (e.isIntersecting) {
				e.target.classList.add('in-view')
				e.target.querySelectorAll('[data-counter]').forEach(animateCounter)
				io.unobserve(e.target)
			}
		})
	},
	{ threshold: 0.12 },
)
document
	.querySelectorAll('.reveal,.reveal-left,.reveal-right')
	.forEach(function (el) {
		io.observe(el)
	})

/* Form */
function handleSubmit() {
	var n = document.getElementById('fname').value.trim()
	var p = document.getElementById('fphone').value.trim()
	if (!n || !p) {
		alert('Пожалуйста, заполните обязательные поля: имя и телефон.')
		return
	}
	document.getElementById('appForm').style.display = 'none'
	document.getElementById('formSuccess').style.display = 'block'
}

/* Smooth scroll */
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
	a.addEventListener('click', function (e) {
		var t = document.querySelector(this.getAttribute('href'))
		if (t) {
			e.preventDefault()
			t.scrollIntoView({ behavior: 'smooth', block: 'start' })
		}
	})
})
/* ============================== MULTILANGUAGE ============================== */
document.addEventListener('DOMContentLoaded', () => {
	const langBtns = document.querySelectorAll('.lang-btn')
	const langEls = document.querySelectorAll('.lang-el')

	// Функция применения языка
	function setLang(lang) {
		langEls.forEach(el => {
			// Проверяем, есть ли перевод для данного элемента
			if (el.getAttribute('data-' + lang)) {
				// Если это поле ввода (input/textarea), меняем placeholder, иначе внутренний HTML
				if (
					el.tagName.toLowerCase() === 'input' ||
					el.tagName.toLowerCase() === 'textarea'
				) {
					el.placeholder = el.getAttribute('data-' + lang)
				} else {
					el.innerHTML = el.getAttribute('data-' + lang)
				}
			}
		})

		// Обновляем активные кнопки во всех переключателях (десктоп и мобайл)
		langBtns.forEach(btn => {
			if (btn.getAttribute('data-lang') === lang) {
				btn.classList.add('active')
			} else {
				btn.classList.remove('active')
			}
		})

		// Сохраняем выбор пользователя в браузере
		localStorage.setItem('schoolLang', lang)
	}

	// Вешаем события на кнопки
	langBtns.forEach(btn => {
		btn.addEventListener('click', e => {
			e.preventDefault()
			setLang(btn.getAttribute('data-lang'))
		})
	})

	// При загрузке страницы проверяем, сохранял ли пользователь язык ранее
	const savedLang = localStorage.getItem('schoolLang') || 'ru'
	setLang(savedLang)
})
document.addEventListener('DOMContentLoaded', () => {
	const langBtns = document.querySelectorAll('.lang-btn')
	const langEls = document.querySelectorAll('.lang-el')
	const toggle = document.getElementById('navToggle')
	const menu = document.getElementById('mobileMenu')

	// Переключение языка
	function setLang(lang) {
		langEls.forEach(el => {
			const translation = el.getAttribute(`data-${lang}`)
			if (translation) el.innerHTML = translation
		})
		langBtns.forEach(btn => {
			btn.classList.toggle('active', btn.dataset.lang === lang)
		})
		localStorage.setItem('selectedLang', lang)
	}

	langBtns.forEach(btn => {
		btn.onclick = () => setLang(btn.dataset.lang)
	})

	// Бургер-меню
	if (toggle) {
		toggle.onclick = () => {
			const isOpen = menu.style.display === 'block'
			menu.style.display = isOpen ? 'none' : 'block'
			toggle.innerHTML = isOpen
				? '<i class="bi bi-list"></i>'
				: '<i class="bi bi-x-lg"></i>'
		}
	}

	// Запуск сохраненного языка
	setLang(localStorage.getItem('selectedLang') || 'ru')
})
