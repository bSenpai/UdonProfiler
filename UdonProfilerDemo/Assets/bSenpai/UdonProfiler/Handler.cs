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
        private Profiler m_Profiler;

        private void Start()
        {
            m_Profiler = GetComponent<Profiler>();
        }

        // End frame at latest time possible.
        public override void PostLateUpdate()
        {
            m_Profiler.EndFrame();
        }
    }
}
