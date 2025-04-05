fx = :level

live_loop :mood_1 do
  use_real_time
  mood_data, sfx = sync "/midi:sound_board_2:1/note_on" # this is how we get input
  mood = mood_data % 10 # this decodes the message using mod maths
  rate = (mood_data - (mood_data % 10)).to_f / 50
  
  # this plays the indented sound
  with_fx fx do
    if mood == 1
      sample :loop_tabla, rate: rate
      sleep 10 / rate
    elsif mood == 2
      sample :loop_breakbeat, rate: rate
      sleep 1.6 / rate
    elsif mood == 3
      sample :loop_weirdo, rate: rate
      sleep 4 / rate
    else
      sample :perc_bell, rate: rate * rrand(-1.5, 1.5)
      sleep rrand(0.1, 2) / rate
    end
  end
end

live_loop :sfx_1 do
  use_real_time
  mood, sfx = sync "/midi:sound_board_2:1/note_on"
  if sfx > 99
    # this chooses a random effect to apply
    fx = [:level, :autotuner, :tanh, :sound_out_stereo, :slicer, :ring_mod, :reverb, :rbpf, :pitch_shift, :ping_pong, :panslicer, :octaver].sample
  end
  sfx = sfx % 100
  if sfx == 1
    sample :mehackit_robot1
    sleep 0.5
  elsif sfx == 2
    sample :vinyl_backspin
    sleep 0.5
  elsif sfx == 3
    sample :drum_cymbal_open
    sleep 0.5
  elsif sfx == 4
    sample :drum_cymbal_open
    sleep 0.5
  elsif sfx == 5
    sample :perc_till
    sleep 0.5
  elsif sfx == 6
    sample :misc_crow
    sleep 0.5
  elsif sfx == 7
    sample :bd_chip
    sleep 0.5
  elsif sfx == 8
    sample :elec_triangle
    sleep 0.5
  end
end
