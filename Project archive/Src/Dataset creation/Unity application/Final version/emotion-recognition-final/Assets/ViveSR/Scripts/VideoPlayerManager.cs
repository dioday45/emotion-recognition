using UnityEngine;
using UnityEngine.Video;
using ViveSR;

public class VideoPlayerManager : MonoBehaviour
{
    private VideoPlayer Vp;
    private int AUNumber = 0;
    private RecordingTimer Timer;
    private const int nbAU = 16; // starting from 1
    public VideoClip[] clip = new VideoClip[nbAU];
    
    
    // Start is called before the first frame update
    void Start()
    {
        Vp = gameObject.GetComponent<VideoPlayer>();
        Timer = FindObjectOfType<RecordingTimer>();
    }

    // Update is called once per frame
    void Update()
    {
        var exprNumber = Timer.expressionNumber;
        if (exprNumber != AUNumber && exprNumber < nbAU)
        {
            AUNumber = exprNumber;
            ChangeClips();
        }
    }

    void ChangeClips()
    {
        Vp.clip = clip[AUNumber];
    }
}
