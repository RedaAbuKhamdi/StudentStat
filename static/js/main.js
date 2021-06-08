function load_lesson_info(){
    let teacher_name = document.getElementById('Teacher').value
    let group_name = document.getElementById('Group').value
    $.get( "/get_lessons", {teacher_name :teacher_name, group_name : group_name} ,function( data ) {
        console.log(data)
      }, 'html');
}