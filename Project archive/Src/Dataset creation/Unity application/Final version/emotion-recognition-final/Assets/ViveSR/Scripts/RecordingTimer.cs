using UnityEngine;
using UnityEngine.UI;
using ViveSR.anipal.Eye;
using ViveSR.anipal.Lip;

namespace ViveSR
{
    public class RecordingTimer : MonoBehaviour
    {
        [HideInInspector] public bool isRecording = false;
        [SerializeField] private float timeValue = 5;
        private Text TimerText;
        private bool IsPreRecording = false;
        private SRanipal_AvatarLipSample_v2 LipSampleV2;
        private SRanipal_AvatarEyeSample_v2 EyeSampleV2;

        public int expressionNumber = 0;
        private const int max_expr_number = 21;

        private void Start()
        {
            if (TimerText == null)
            {
                TimerText = GetComponent<Text>();
            }

            LipSampleV2 = FindObjectOfType<SRanipal_AvatarLipSample_v2>();
            EyeSampleV2 = FindObjectOfType<SRanipal_AvatarEyeSample_v2>();
        }

        // Update is called once per frame
        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.Return))
            {
                IsPreRecording = true;
            }
            
            if (IsPreRecording)
            {
                PreRecording();
            }

            if (isRecording)
            {
                Recording();
            }

            if(!(isRecording || IsPreRecording)){
                if(Input.GetKeyDown(KeyCode.LeftArrow)){
                    if(expressionNumber > 0){
                        --expressionNumber;
                        LipSampleV2.MultipleExpressionTracking = 0;
                        EyeSampleV2.MultipleExpressionTracking = 0;
                    }
                }
                else if (Input.GetKeyDown(KeyCode.RightArrow)){
                    if(expressionNumber < max_expr_number){
                        ++expressionNumber;
                        LipSampleV2.MultipleExpressionTracking = 0;
                        EyeSampleV2.MultipleExpressionTracking = 0;

                    }

                }
            }

            bool apex = Input.GetKeyDown(KeyCode.Space);
            LipSampleV2.IsApex = apex;
            EyeSampleV2.IsApex = apex;
            DisplayCounter(timeValue);
            

        }

        /// <summary>
        /// Subject preparation for 5 second (decreasing counter)
        /// </summary>
        private void PreRecording()
        {
            if (timeValue > 0)
            {
                timeValue -= Time.deltaTime;
            }
            else
            {
                TimerText.color = Color.red;
                IsPreRecording = false;
                isRecording = true;
            }
        }

        /// <summary>
        /// Increase timeValue until 3 second
        /// </summary>
        private void Recording()
        {
            if (timeValue < 5)
            {
                timeValue += Time.deltaTime;
            }
            else
            {
                isRecording = false;
                TimerText.color = Color.black;
            }
        }

        /// <summary>
        /// Display timeToDisplay on the format 00:00
        /// </summary>
        /// <param name="timeToDisplay"></param>
        private void DisplayCounter(float timeToDisplay)
        {
            timeToDisplay = (timeToDisplay < 0) ? 0 : timeToDisplay;
            float seconds = Mathf.FloorToInt(timeToDisplay % 60);
            TimerText.text = string.Format("Expression number : {0} \n Timer : {1:00}:{2:00}", expressionNumber, 0f, seconds);
        }
    }
}