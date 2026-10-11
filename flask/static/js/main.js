const toggleMobileMenu = (menu) => {
  menu.classList.toggle('open');
  menu.querySelector('.menu-toggle').setAttribute('aria-expanded', menu.classList.contains('open'));
};

const closeMobileMenu = (menu) => {
  menu.classList.remove('open');
  menu.querySelector('.menu-toggle').setAttribute('aria-expanded', 'false');
};

const mobileMenu = document.getElementById('hamburger-icon');
const mobileLayout = window.matchMedia('(max-width: 800px)');

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && mobileMenu.classList.contains('open')) {
    closeMobileMenu(mobileMenu);
    if (mobileLayout.matches) {
      mobileMenu.querySelector('.menu-toggle').focus();
    }
  }
});

mobileMenu.addEventListener('focusout', (event) => {
  if (!mobileMenu.contains(event.relatedTarget)) {
    closeMobileMenu(mobileMenu);
  }
});

mobileLayout.addEventListener('change', (event) => {
  if (!event.matches) {
    closeMobileMenu(mobileMenu);
  }
});

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

const collapseHeader = (toggler, table, className) => {
  const headRow = table.getElementsByClassName(className)[0];
  if (headRow.classList.contains('active')) {
    headRow.classList.remove('active');
    toggler.setAttribute('value', 'Hide');
  } else {
    headRow.classList.add('active');
    toggler.setAttribute('value', 'Show');
  }
  toggler.setAttribute('aria-expanded', !headRow.classList.contains('active'));
  toggler.setAttribute('aria-label', toggler.value + ' ' + toggler.dataset.tableLabel);
}

const collapseBody = (table, className) => {

  const bodyRows = table.getElementsByClassName(className);
  for (var i = 0; i < bodyRows.length; i++) {
    const bodyRow = bodyRows[i];
    if (bodyRow.classList.contains('active')) {
      bodyRow.classList.remove('active');
    } else {
      bodyRow.classList.add('active');
    }
  }
}
const collapseBettiAndEulerTable = (toggler) => {
  const element = document.getElementById('BettiAndEulerTable');

  collapseHeader(toggler, element, 'BettiAndEulerHeadRow');

  collapseBody(element, 'BettiAndEulerBodyRow');
}

const collapseStatisticsTable = (toggler) => {
  const element = document.getElementById('StatisticsTable');

  collapseHeader(toggler, element, 'StatisticsHeadRow');

  collapseBody(element, 'StatisticsBodyRow');
}

const collapseRatiosTable = (toggler) => {
  const element = document.getElementById('RatiosTable');

  collapseHeader(toggler, element, 'RatiosHeadRow');

  collapseBody(element, 'RatiosBodyRow');
}

const collapseRawDataTable = (toggler) => {
  const element = document.getElementById('RawDataTable');

  collapseHeader(toggler, element, 'RawDataHeadRow');

  collapseBody(element, 'RawDataBodyRow');
}

window.addEventListener('scroll', scrollFunction, { passive: true });

function scrollFunction() {
  const button = document.getElementById('GoToTopButton');
  const scrolled = document.body.scrollTop > 20 || document.documentElement.scrollTop > 20;
  const visible = scrolled || document.activeElement === button;
  button.hidden = !visible;
  button.style.bottom = visible ? '0' : '-100px';
}

document.getElementById('GoToTopButton').addEventListener('blur', scrollFunction);
scrollFunction();
