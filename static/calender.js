$('.date').on('dblclick',(event)=>{
    hidden_year = parseInt(document.getElementById('year-hidden').textContent);
    hidden_month = parseInt(document.getElementById('month-hidden').textContent);
    let day = event.target.textContent;
    
    // event.target.outerHTML = `<div class="date center overflowsign">&#10003;</div>`
    event.target.outerHTML = `<div class="date center overflowsign">&#10007;</div>`
    console.log('clicked');
    
    let d = new Date();
    let currentMonth = d.getMonth() + 1;
    let currentYear = d.getFullYear();
    // let key = day+'-'+currentMonth+'-'+currentYear;
    data = {}
    data['day'] = day;
    data['month'] = hidden_month;
    data['year'] = hidden_year;
    console.log('sending data', year, month, day);
    $.ajax({
        type: 'POST',
        url: "/",
        contentType: 'application/text',
        data : data
    })
})
    
