// MIT License
// Copyright (c) 2021 Merlin
// Source: https://gist.github.com/MerlinVR/2da80b29361588ddb556fd8d3f3f47b5

using UdonSharp;
using UnityEngine;

namespace bSenpai.UdonProfiler
{
    // Have profiler start frame timing before any other script runs.
    [DefaultExecutionOrder(-2_000_000_000)]
    [UdonBehaviourSyncMode(BehaviourSyncMode.None)]
    public class Kickoff : UdonSharpBehaviour
    {
        private Profiler m_Profiler;

        private int m_CurrentFrame = -1;

        private void Start()
        {
            m_Profiler = GetComponent<Profiler>();

            if (m_Profiler == null)
            {
                Debug.LogError("Profiler script not attached to game object!");
            }
        }

        // Begin frame at earliest time possible.
        private void FixedUpdate()
        {
            if (m_Profiler && m_Profiler.ScriptEnabled)
            {
                if (m_CurrentFrame != Time.frameCount)
                {
                    m_CurrentFrame = Time.frameCount;
                    if (!m_Profiler.InFrame)
                    {
                        m_Profiler.BeginFrame();
                    }
                }

                m_Profiler.BeginSample("FixedUpdate");
            }
        }

        private void Update()
        {
            if (m_Profiler && m_Profiler.ScriptEnabled)
            {
                m_Profiler.BeginSample("Update");
            }
        }

        private void LateUpdate()
        {
            if (m_Profiler && m_Profiler.ScriptEnabled)
            {
                m_Profiler.BeginSample("LateUpdate");
            }
        }

        public override void PostLateUpdate()
        {
            if (m_Profiler && m_Profiler.ScriptEnabled)
            {
                m_Profiler.BeginSample("PostLateUpdate");
            }
        }
    }
}
