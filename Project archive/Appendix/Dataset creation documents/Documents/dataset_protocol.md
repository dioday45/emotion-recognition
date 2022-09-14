# Protocol for creating the emotion recognition database based on CK+

## Type of subject

- 20-30 subjects should be fine
- Different ethnocity
- Different ages, from 18 to 60
- Different visage shapes
- Include people with glasses, lenses, beard or jewelry 

## What type of recording

For each expression asked to the subject, we would start the recording at neutral state, pass the apex state and end at a neutral state.

Records blendshapes value at 30Hz.

## First recording - 16 single AU

At first, subject should reproduce each one of the 16 AUs from the table below. 

To describe the expression to the subject we can use this website : https://imotions.com/blog/facial-action-coding-system/

|          |                      |                                                 |                                                              |                            |
| -------- | -------------------- | ----------------------------------------------- | ------------------------------------------------------------ | -------------------------- |
| **AUs ** | **AUs Definition**   | **corresponding Blend shapes**                  | **Blendshapes definitions**                                  | **Comments**               |
| AU 1     | Inner Brow Raiser    | Eye_Left_Up and Eye_Right_Up                    | Influences the muscles around  the eye, moving these muscles further upward with a higher value. | /                          |
| AU 2     | Outer Brow Raiser    | Eye_Right_Left or Eye_Left_Left                 | influences the muscles around  the left eye, moving these muscles further lef/rightward with a higher value. | /                          |
| AU 4     | Brow Lowerer         | Eye_Left_Down and Eye_Right_Down                | influences the muscles around  the left eye, moving these muscles further downward with a higher value. | /                          |
| AU 5     | Upper Lid Raiser     | Eye_Left_Wide and Eye_Right_Wide                | open avatar’s right eye wide, it  should be done when Eye_Blink_Right = 0. | /                          |
| AU 6     | Cheek Raiser         | /                                               | /                                                            | /                          |
| AU 7     | Lid Tightener        | Eye_Left_Blink and Eye_Right_Blink              | influences blinking of the left  eye, closing it further with a higher value. | determine value (not 100%) |
| AU 9     | Nose Wrinkler        | /                                               | /                                                            | showed by AU10             |
| AU 10    | Upper Lip Raiser     | Mouth_UpperRight_Up +  Mouth_UpperLeft_Up       | Lowers the left/right upper lip  further with a higher value. | /                          |
| AU 12    | Lip Corner Puller    | Mouth_Smile_Right and Mouth_Smile_Left          | raises the left/right side of  the mouth further with a higher value. | /                          |
| AU 14    | Dimpler              | /                                               | /                                                            | /                          |
| AU 15    | Lip Corner Depressor | Mouth_Sad_Right and  Mouth_Sad_Left             | lowers the left/right side of  the mouth further with a higher value. | /                          |
| AU 16    | Lower Lip Depressor  | Mouth_Lower_DownRight and  Mouth_Lower_DownLeft | lowers the left/right lower lip  further with a higher value. | /                          |
| AU 17    | Chin Raiser          | Mouth_Lower_Overlay                             | stretches the lower lip further  and lays it on the upper lip further with a higher value. | not really accurate        |
| AU 20    | Lip stretcher        | /                                               | /                                                            | /                          |
| AU 23    | Lip Tightener        | Mouth_Pout                                      | allows the lips to pout more  with a higher value.           | not really accurate        |
| AU 26    | Jaw Drop             | Jaw_Open                                        | opens the mouth further with the  higher value.              | determine value (not 100%) |

## Second recording - Combination of AU

For the second part of the recording, the subject should express a combination of selected AUs that are representing the 6 basic emotions : Happiness, Sadness, Anger, Fear, Disgust and Surprise.

## Recording sample

One sample should have the following parameters :

| Subject number | Session number | Frame number | AU asked | Emotion asked | Blendshapes ... |
| :------------- | -------------- | ------------ | -------- | ------------- | --------------- |
