using UnityEngine;
using UnityEngine.UI;
using ViveSR.anipal.Lip;

public class LipsVideoManager : MonoBehaviour
{
    // Start is called before the first frame update
    private RawImage image;
    private Texture2D texture;
    void Start()
    { 
        image = GetComponent<RawImage>();
        texture = new Texture2D(SRanipal_Lip_v2.ImageWidth, SRanipal_Lip_v2.ImageHeight, TextureFormat.R8, false);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if (SRanipal_Lip_v2.GetLipImage(ref texture))
        {
            image.texture = texture;
        }
    }
}
