using bSenpai.UdonProfiler;
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

namespace bSenpai
{

    [UdonBehaviourSyncMode(BehaviourSyncMode.None)]
    public class GameManager : UdonSharpBehaviour
    {
        private Profiler m_Profiler = null;

        void Start()
        {
            var profilerGo = GameObject.Find("Profiler");
            if (profilerGo == null)
            {
                Debug.LogError("Profiler object not found in scene!");
                return;
            }

            m_Profiler = profilerGo.GetComponent<Profiler>();
        }

        private void FixedUpdate()
        {
            if (m_Profiler)
            {
                m_Profiler.BeginSample("Loop A");
                PrintLoop("Hello Loop A", 10);

                m_Profiler.BeginSample("A");
                PrintLoop("A", 10);
                m_Profiler.EndSample();

                m_Profiler.EndSample();
            }
        }

        private void Update()
        {
            if (m_Profiler)
            {
                m_Profiler.BeginSample("Loop B");
                PrintLoop("Hello Loop B", 10);
                m_Profiler.EndSample();
            }
        }

        private void LateUpdate()
        {
            if (m_Profiler)
            {
                m_Profiler.BeginSample("Loop C");
                PrintLoop("Hello Loop C", 10);
                m_Profiler.EndSample();
            }
        }

        public override void PostLateUpdate()
        {
            if (m_Profiler)
            {
                m_Profiler.BeginSample("Loop D");
                PrintLoop("Hello Loop D", 10);
                m_Profiler.EndSample();
            }
        }

        private void PrintLoop(string msg, int iterations)
        {
            for (int i = 0; i < iterations; i++)
            {
                Debug.Log(msg);
            }
        }
    }
}
