## General Form of Commands

`(cmd arg1 arg2)`

`(+ 13 (/ 21 3) (* 2.5 2))`

`(param-disp 'laser1)`

`(param-ref 'int-param)`

`(param-set! 'int-param 50)`

### Goals of communication with the DLC

Be able to set all lock parameters and monitor stabilization. Display and explain errors and how we fixed them.

Potentially merge the communication with the DLC with communication with the TC-200 temperature controller and with the oscilloscope, in a time syncronized fashion.

## Some Useful commands

`(param-disp 'laser1)`

`(param-ref 'laser1:emission)`

`(param-ref 'laser1:dl:ontime-txt)`

`(param-set! 'laser1:dl:cc:enabled #t)`
To turn the emission on or off, if the other requirements are satisfied

`(param-ref 'laser1:dl:cc:current-act)`

`(param-ref 'laser1:dl:tc:temp-act)`

`(param-ref 'laser1:dl:dc:voltage-act)`

`(param-ref 'laser1:scope:data)` --> needs decoding into float array data


The labview vi runs on an internal loop of 100 ms, which it stops for 500 ms when sending a command. When the loop is stopped, a command is called to close the connection.