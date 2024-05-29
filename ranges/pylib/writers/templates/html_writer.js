document.querySelector('table.text thead')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const cls = event.target.classList;
        const trs = document.querySelectorAll('table.text tr.term');
        const buttons = document.querySelectorAll('table.text button.toggle');
        if (cls.contains('closed')) {
            trs.forEach(function(tr) {  tr.classList.remove('closed'); });
            buttons.forEach(function(b) {  b.classList.remove('closed'); });
        } else {
            trs.forEach(function(tr) {  tr.classList.add('closed'); });
            buttons.forEach(function(b) {  b.classList.add('closed'); });
        }
 });

document.querySelector('table.text tbody')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const textId = event.target.dataset.textId;
        const selector = `[data-text-id="${textId}"]`;
        const elts = document.querySelectorAll(selector);
        elts.forEach(function(tr) {  tr.classList.toggle('closed'); });
    });

document.querySelector('table.counts thead')
    .addEventListener('click', function(event) {
        const elts = document.querySelectorAll(".summary");
        elts.forEach(function(tr) {  tr.classList.toggle('closed'); });
    });
