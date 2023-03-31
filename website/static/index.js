function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function modifyNote(noteId) {
    var textarea = document.getElementById("note");
    var content = textarea.value;
    content = content.split("|")
    var new_title = content[0]
    var new_latex = content[1]
    var new_explanation = content[2] 
  fetch("/modify-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId, new_title: new_title,new_latex: new_latex, new_explanation: new_explanation }),
  }).then((_res) => {
    window.location.href = "/";
  });
  }