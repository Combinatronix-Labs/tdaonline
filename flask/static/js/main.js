const toggleMobileMenu = (menu) => {
  menu.classList.toggle('open');
};

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
  element = document.getElementById('BettiAndEulerTable');

  collapseHeader(toggler, element, 'BettiAndEulerHeadRow');

  collapseBody(element, 'BettiAndEulerBodyRow');
}

const collapseStatisticsTable = (toggler) => {
  element = document.getElementById('StatisticsTable');

  collapseHeader(toggler, element, 'StatisticsHeadRow');

  collapseBody(element, 'StatisticsBodyRow');
}

const collapseRatiosTable = (toggler) => {
  element = document.getElementById('RatiosTable');

  collapseHeader(toggler, element, 'RatiosHeadRow');

  collapseBody(element, 'RatiosBodyRow');
}

const collapseRawDataTable = (toggler) => {
  element = document.getElementById('RawDataTable');

  collapseHeader(toggler, element, 'RawDataHeadRow');

  collapseBody(element, 'RawDataBodyRow');
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("GoToTopButton").style.bottom = "0";
  } else {
    document.getElementById("GoToTopButton").style.bottom = "-100px";
  }
}