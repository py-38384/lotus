function get_Local_Time_From_Seconds(input_seconds) {
  const day_standard_in_second = 24 * 60 * 60;
  const hour_standard_in_second = 60 * 60;
  const minute_standard_in_second = 60;
  let output_days = 0;
  let output_hours = 0;
  let output_minutes = 0;
  let output_seconds = 0;
  let output_years = 0;

  output_seconds = input_seconds % 60;
  input_seconds -= output_seconds;
  if (input_seconds >= 60) {
    output_minutes = input_seconds / 60;
    if (output_minutes >= 60) {
      let temp_minutes = output_minutes % 60;
      output_minutes -= temp_minutes;
      output_hours = output_minutes / 60;
      output_minutes = temp_minutes;
      if (output_hours >= 24) {
        let temp_hours = output_hours % 24;
        output_hours -= temp_hours;
        output_days = output_hours / 24;
        output_hours = temp_hours;
        if (output_days >= 365) {
          let temp_days = output_days % 365;
          output_days -= temp_days;
          output_years = output_days / 365;
          output_days = temp_days;
        }
      }
    }
  }
  return {
    year: output_years,
    day: output_days,
    hour: output_hours,
    minute: output_minutes,
    second: output_seconds,
  };
}
function set_interval(time_left_sec, element_class) {
  let local_time = {};
  let time_string = "";
  const my_interval = setInterval(() => {
    local_time = get_Local_Time_From_Seconds(time_left_sec);
    if (local_time.year > 0) {
      time_string += `${local_time.year} year `;
    }
    if (local_time.day) {
      time_string += `${local_time.day}  day `;
    }
    if (local_time.hour) {
      time_string += `${local_time.hour}  hour `;
    }
    if (local_time.minute) {
      time_string += `${local_time.minute}  minute `;
    }
    if (local_time.second) {
      time_string += `${local_time.second}  second `;
    }

    document.querySelector(`.${element_class}`).innerHTML = time_string
    time_left_sec -= 1;
    time_string = "";
    if (time_left_sec <= 0) {
        clearInterval(my_interval);
        window.location = window.location.href;
    }
  }, 1000);
}

if(typeof email_resend_time_left_sec !== 'undefined'){
    set_interval(email_resend_time_left_sec,'resend-unavailable')
}
if(typeof input_active_time_left_sec !== 'undefined'){
    set_interval(input_active_time_left_sec,'input-unavailable')
}