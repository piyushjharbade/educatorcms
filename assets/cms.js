$(document).ready(function(){
 $.getJSON("/displayallcoursejson",function(data){
    $.each(data,function(index,item){
       $('#cid').append($('<option>').text(item[1]).val(item[0]))

    } )
 })

  $('#cid').change(function(){
     $('#did').empty()
     $('#did').append($('<option>').text("-Select Department-"))
     $.getJSON("/displayalldepartmentjson",{cid:$('#cid').val()},function(data){
       $.each(data,function(index,item){
         $('#did').append($('<option>').text(item[2]).val(item[1]))
       })

     })

  })

  $('#did').change(function(){
     $('#sid').empty()
     $('#sid').append($('<option>').text("-Select Subject-"))
     $.getJSON("/displayallsubjectjson",{did:$('#did').val()},function(data){
       $.each(data,function(index,item){
         $('#sid').append($('<option>').text(item[3]).val(item[2]))
       })

     })

  })

  $.getJSON('/fetchallteacher',function(data){
    $.each(data,function(index,item){
      $('#tchrid').append($('<option>').text(item[1]).val(item[0]))
    })
  })

    $.getJSON('/fetchallstudent',function(data){
    $.each(data,function(index,item){
      $('#stuid').append($('<option>').text(item[1]).val(item[0]))
    })
  })

      $.getJSON('/fetchallsubject',function(data){
    $.each(data,function(index,item){
      $('#subjectid').append($('<option>').text(item[3]).val(item[2]))
    })
  })

    $('#subjectid').change(function(){
     $('#teacherid').empty()
     $('#teacherid').append($('<option>').text("-Select Teacher-"))
     $.getJSON("/enrollstudentjson",{subjectid:$('#subjectid').val()},function(data){
       $.each(data,function(index,item){
         $('#teacherid').append($('<option>').text(item[5]).val(item[1]))
       })

     })

  })


})
$(document).ready(function(){
  $('#cid').change(function(){
     $('#bid').empty()
     $('#bid').append($('<option>').text("-Select Branch-"))
     $.getJSON("/displayallbranchjson",{cid:$('#cid').val()},function(data){
       $.each(data,function(index,item){
         $('#bid').append($('<option>').text(item[2]).val(item[1]))
       })

     })

  })


})