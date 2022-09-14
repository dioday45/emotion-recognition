//========= Copyright 2019, HTC Corporation. All rights reserved. ===========
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text;
using System;
using UnityEngine.Serialization;

namespace ViveSR
{
    namespace anipal
    {
        namespace Lip
        {
            public class SRanipal_AvatarLipSample_v2 : MonoBehaviour
            {
                [SerializeField] private List<LipShapeTable_v2> LipShapeTables;
                [SerializeField] private int subjectNumber = 0;
                

                public bool NeededToGetData = true;
                private Dictionary<LipShape_v2, float> LipWeightings;

                private const  int NbExpression = 21; //starting from 0
                private const string LipsPath = "Assets/Data/Weights/lips_blendshapes.csv";

                //Recording attributes
                public int expressionNumber = 0;
                public int MultipleExpressionTracking = 0;
                private int FrameCounter = 0;
                private bool EnableMultipleExpression = false;
                public bool IsApex = false;
                private enum Expressions
                {
                    AU1,
                    AU2,
                    AU4,
                    AU5,
                    AU6,
                    AU7,
                    AU9,
                    AU10,
                    AU12,
                    AU14,
                    AU15,
                    AU16,
                    AU17,
                    AU20,
                    AU23,
                    AU26,
                    Happy,
                    Sad,
                    Angry,
                    Fear,
                    Disgust,
                    Surprise
                }
                
                //recording timer
                private RecordingTimer RecordingTimer;

                private void Start()
                {
                    if (!SRanipal_Lip_Framework.Instance.EnableLip)
                    {
                        enabled = false;
                        return;
                    }
                    SetLipShapeTables(LipShapeTables);
                    RecordingTimer = FindObjectOfType<RecordingTimer>();
                }

                private void FixedUpdate()
                {
                    if (SRanipal_Lip_Framework.Status != SRanipal_Lip_Framework.FrameworkStatus.WORKING) return;

                    if (NeededToGetData)
                    {
                        SRanipal_Lip_v2.GetLipWeightings(out LipWeightings);
                        UpdateLipShapes(LipWeightings);
                    }

                    /*
                    Recording
                    */
                    if (RecordingTimer.isRecording && EnableMultipleExpression)
                    {
                        ++MultipleExpressionTracking;
                        EnableMultipleExpression = false;
                    }
                    if(!RecordingTimer.isRecording)
                    {
                        EnableMultipleExpression = true;
                        FrameCounter = 0;
                    }
                    

                    if (RecordingTimer.isRecording)
                    {
                        WriteLipBlendshapes(LipWeightings);
                        ++FrameCounter;
                    }
                    expressionNumber = RecordingTimer.expressionNumber;
                    
                }
                

                public void SetLipShapeTables(List<LipShapeTable_v2> lipShapeTables)
                {
                    bool valid = true;
                    if (lipShapeTables == null)
                    {
                        valid = false;
                    }
                    else
                    {
                        for (int table = 0; table < lipShapeTables.Count; ++table)
                        {
                            if (lipShapeTables[table].skinnedMeshRenderer == null)
                            {
                                valid = false;
                                break;
                            }
                            for (int shape = 0; shape < lipShapeTables[table].lipShapes.Length; ++shape)
                            {
                                LipShape_v2 lipShape = lipShapeTables[table].lipShapes[shape];
                                if (lipShape > LipShape_v2.Max || lipShape < 0)
                                {
                                    valid = false;
                                    break;
                                }
                            }
                        }
                    }
                    if (valid)
                        LipShapeTables = lipShapeTables;
                }

                public void UpdateLipShapes(Dictionary<LipShape_v2, float> lipWeightings)
                {
                    foreach (var table in LipShapeTables)
                        RenderModelLipShape(table, lipWeightings);
                }

                private void RenderModelLipShape(LipShapeTable_v2 lipShapeTable, Dictionary<LipShape_v2, float> weighting)
                {
                    for (int i = 0; i < lipShapeTable.lipShapes.Length; i++)
                    {
                        int targetIndex = (int)lipShapeTable.lipShapes[i];
                        if (targetIndex > (int)LipShape_v2.Max || targetIndex < 0) continue;
                        lipShapeTable.skinnedMeshRenderer.SetBlendShapeWeight(i, weighting[(LipShape_v2)targetIndex] * 100);
                    }
                }

                /// <summary>
                /// write lips blendshapes values into the corresponding .csv file 
                /// </summary>
                /// <returns> void </returns>
                private void WriteLipBlendshapes(Dictionary<LipShape_v2, float>  lipWeightings){
                    var csv = new StringBuilder();
                    var newLine = string.Format("{0},{1},{2},{3},{4}", subjectNumber.ToString(),
                        ((Expressions) expressionNumber).ToString(), MultipleExpressionTracking.ToString(), FrameCounter.ToString(), IsApex.ToString());
                    
                    foreach (var weights in lipWeightings)
                    {
                        newLine += String.Format(",{0}", Convert.ToSingle(weights.Value));
                    }

                    csv.AppendLine(newLine);
                    File.AppendAllText(LipsPath, csv.ToString());
                }

            }
        }
    }
}