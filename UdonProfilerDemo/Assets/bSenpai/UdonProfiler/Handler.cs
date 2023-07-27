// MIT License
// Copyright (c) 2021 Merlin
// Source: https://gist.github.com/MerlinVR/2da80b29361588ddb556fd8d3f3f47b5

using UdonSharp;
using UnityEngine;

namespace bSenpai.UdonProfiler
{
    // Have profiler end frame timing after all scripts run.
    [DefaultExecutionOrder(2_000_000_000)]
    [UdonBehaviourSyncMode(BehaviourSyncMode.None)]
    public class Handler : UdonSharpBehaviour
    {
        private Profiler m_Profiler = null;

        private void Start()
        {
            m_Profiler = GetComponent<Profiler>();

            if (m_Profiler == null)
            {
                Debug.LogError("Profiler script not attached to game object!");
            }
        }

        private void FixedUpdate()
        {
            if (m_Profiler)
            {
                m_Profiler.EndSample();
            }
        }

        private void Update()
        {
            if (m_Profiler)
            {
                m_Profiler.EndSample();
            }
        }

        private void LateUpdate()
        {
            if (m_Profiler)
            {
                m_Profiler.EndSample();
            }
        }

        // End frame at latest time possible.
        public override void PostLateUpdate()
        {
            if (m_Profiler)
            {
                m_Profiler.EndSample();

                m_Profiler.EndFrame();
            }
        }
    }
}
