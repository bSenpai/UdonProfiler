using UnityEngine;

using UdonSharp;

using VRC.SDK3.Data;

using sample_t = VRC.SDK3.Data.DataDictionary;

namespace bSenpai.UdonProfiler
{
    [UdonBehaviourSyncMode(BehaviourSyncMode.None)]
    public class Profiler : UdonSharpBehaviour
    {
        public bool ScriptEnabled = true;

        private sample_t m_FrameSample = null;

        private sample_t m_CurrentSample = null;

        private int m_CurrentFrame = -1;

        // Check if we are in a frame before recording info.
        private bool m_InFrame = false;

        public bool InFrame { get { return m_InFrame; } }

        public void BeginFrame()
        {
            if (!ScriptEnabled || m_InFrame)
            {
                return;
            }

            m_InFrame = true;

            m_CurrentFrame++;

            sample_t frameSample = Sample.New("UdonBehaviour");

            frameSample.SetParent(Sample.New(""));
            frameSample.SetPathName("/UdonBehaviour");
            frameSample.IncrementNumCalls();

            m_FrameSample = frameSample;

            m_CurrentSample = frameSample;

            frameSample.AddStartTime();
        }

        public void EndFrame()
        {
            if (!ScriptEnabled || !m_InFrame)
            {
                return;
            }

            sample_t frameSample = m_FrameSample;

            frameSample.AddEndTime();

            CalculateFrameTimes();

            OutputFrameInfo();

            m_InFrame = false;
        }

        private void CalculateFrameTimes()
        {
            sample_t frameSample = m_FrameSample;

            frameSample.CalculateTimes(0);
            double frameTime = frameSample.GetTotalTimeMs();

            CalculateAllTimes(frameSample, frameTime);
        }

        [RecursiveMethod]
        private void CalculateAllTimes(sample_t curSample, double frameTime)
        {
            DataDictionary children = curSample.GetChildren();
            DataList keys = children.GetKeys();
            for (int i = 0; i < keys.Count; i++)
            {
                sample_t child = curSample.GetChild(keys[i].String);
                child.CalculateTimes(frameTime);
                CalculateAllTimes(child, frameTime);
            }
        }

        private void OutputFrameInfo()
        {
            string frameInfo = EncodeFrame(m_FrameSample);

            // First recorded frame time is inaccurate since it accounts for application setup time.
            if (m_CurrentFrame > 0)
            {
                Debug.Log(
                    "##FRAME_INFO_BEGIN##\n" +
                    frameInfo +
                    "##FRAME_INFO_END##"
                );
            }
        }

        [RecursiveMethod]
        private string EncodeFrame(sample_t curSample)
        {
            DataDictionary children = curSample.GetChildren();
            DataList keys = children.GetKeys();
            string printString = "";
            for (int i = 0; i < keys.Count; i++)
            {
                string key = keys[i].String;
                printString += EncodeFrame(children[key].DataDictionary);
            }

            string curString = curSample.Encode();

            return curString + printString;
        }

        public void BeginSample(string name)
        {
            if (!ScriptEnabled || !m_InFrame)
            {
                return;
            }

            sample_t parentSample = m_CurrentSample;

            parentSample.AddEndTime();

            DataDictionary parentChildren = parentSample.GetChildren();
            if (!parentChildren.ContainsKey(name))
            {
                parentSample.AddChild(name);
            }
            m_CurrentSample = parentSample.GetChild(name);

            m_CurrentSample.IncrementNumCalls();

            m_CurrentSample.AddStartTime();
        }

        public void EndSample()
        {
            if (!ScriptEnabled || !m_InFrame)
            {
                return;
            }

            m_CurrentSample.AddEndTime();

            sample_t parentSample = m_CurrentSample.GetParent();

            parentSample.AddStartTime();

            m_CurrentSample = parentSample;
        }
    }
}
