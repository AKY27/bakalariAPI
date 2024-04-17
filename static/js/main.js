days = {1:"Pondělí", 2:"Úterý", 3:"Středa", 4:"Čtvrtek", 5:"Pátek"}

function draw_table(data) {
    var rows = data['Days'].length;
    var columns = data['Hours'].length;
    var tableHTML = '<table id="table" border="1"><thead><tr>';

    // Generating column headers
    tableHTML += '<th></th>';
    for (var i = 0; i < columns; i++) {
      tableHTML += `<th>${data.Hours[i].BeginTime}-${data.Hours[i].EndTime}</th>`;
    }
    tableHTML += '</tr></thead><tbody>';

    // Generating table rows
    for (var j = 1; j <= rows; j++) {
      tableHTML += '<tr><th>' + days[j] + '</th>';
      for (var k = 1; k <= columns; k++) {
        try{
          var lesson = data.Days[j-1].Atoms[data.Days[j-1].Atoms.findIndex(obj => obj.HourId === k+2)]
          var sub = data.Subjects[data.Subjects.findIndex(obj => obj.Id === lesson.SubjectId)].Abbrev
          var teach = data.Teachers[data.Teachers.findIndex(obj => obj.Id === lesson.TeacherId)].Abbrev
          var room = data.Rooms[data.Rooms.findIndex(obj => obj.Id === lesson.RoomId)].Abbrev
          tableHTML += `<td><p id="par" align="right">${room}</p><p id="par" align="center">${sub}</p><p id="par" align="center">${teach}</p></td>`;
        }
        catch(err){
          tableHTML += "<td><br><br><br><br></td>"
        }
      }
      tableHTML += '</tr>';
    }

    tableHTML += '</tbody></table>';
    document.getElementById('tableContainer').innerHTML = tableHTML; 
}

fetch("/api/actual/today")
    .then(response => response.json())
    .then(data => {draw_table(data);})
    .catch(error =>{
        console.error('Error fetching JSON:', error);
    });