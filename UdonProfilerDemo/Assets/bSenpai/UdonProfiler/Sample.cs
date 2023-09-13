using UnityEngine;

using VRC.SDK3.Data;

using sample_t = VRC.SDK3.Data.DataDictionary;

namespace bSenpai.UdonProfiler
{
    public static class Sample
    {
        // Class attributes.
        private const string NAME               = "name";
        private const string PATH_NAME          = "pathName";
        private const string PARENT             = "parent";
        private const string CHILDREN           = "children";

        private const string START_TIMES        = "startTimes";
        private const string END_TIMES          = "endTimes";

        private const string TOTAL_TIME_PERCENT = "totalTimePercent";
        private const string TOTAL_TIME_MS      = "totalTimeMilliseconds";
        private const string SELF_TIME_PERCENT  = "selfTimePercent";
        private const string SELF_TIME_MS       = "selfTimeMilliseconds";
        private const string NUM_CALLS          = "numCalls";

        public static sample_t New(string name)
        {
            sample_t self = new DataDictionary();

            self[NAME] = name;
            self[CHILDREN] = new DataDictionary();

            self[START_TIMES] = new DataList();
            self[END_TIMES] = new DataList();

            self[TOTAL_TIME_PERCENT] = 0f;
            self[TOTAL_TIME_MS] = 0f;
            self[SELF_TIME_PERCENT] = 0f;
            self[SELF_TIME_MS] = 0f;
            self[NUM_CALLS] = 0;

            return self;
        }

        public static string GetName(this sample_t self)
        {
            return self[NAME].String;
        }

        public static void SetPathName(this sample_t self, string value)
        {
            self[PATH_NAME] = value;
        }

        public static string GetPathName(this sample_t self)
        {
            return self[PATH_NAME].String;
        }

        public static void SetParent(this sample_t self, sample_t value)
        {
            self[PARENT] = value;
        }

        public static sample_t GetParent(this sample_t self)
        {
            return self[PARENT].DataDictionary;
        }

        public static void AddChild(this sample_t self, string name)
        {
            DataDictionary children = self.GetChildren();
            sample_t child = Sample.New(name);
            child.SetParent(self);
            child.SetPathName(self.GetPathName() + "/" + name);
            children[name] = child;
        }

        public static sample_t GetChild(this sample_t self, string name)
        {
            DataDictionary children = self.GetChildren();
            if (!children.ContainsKey(name))
            {
                Debug.LogError($"{self.GetName()} does not have a child named {name}");
                return Sample.New("");
            }
            return children[name].DataDictionary;
        }

        public static DataDictionary GetChildren(this sample_t self)
        {
            return self[CHILDREN].DataDictionary;
        }

        public static void AddStartTime(this sample_t self)
        {
            DataList startTimes = self.GetStartTimes();
            startTimes.Add(Time.realtimeSinceStartup * 1000);
        }

        public static DataList GetStartTimes(this sample_t self)
        {
            return self[START_TIMES].DataList;
        }

        public static void AddEndTime(this sample_t self)
        {
            DataList endTimes = self.GetEndTimes();
            endTimes.Add(Time.realtimeSinceStartup * 1000);
        }

        public static DataList GetEndTimes(this sample_t self)
        {
            return self[END_TIMES].DataList;
        }

        public static void SetTotalTimeMs(this sample_t self, double value)
        {
            self[TOTAL_TIME_MS] = value;
        }

        public static double GetTotalTimeMs(this sample_t self)
        {
            return self[TOTAL_TIME_MS].Double;
        }

        public static void SetSelfTimeMs(this sample_t self, double value)
        {
            self[SELF_TIME_MS] = value;
        }

        public static double GetSelfTimeMs(this sample_t self)
        {
            return self[SELF_TIME_MS].Double;
        }

        public static void SetTotalTimePercent(this sample_t self, float value)
        {
            self[TOTAL_TIME_PERCENT] = value;
        }

        public static float GetTotalTimePercent(this sample_t self)
        {
            return self[TOTAL_TIME_PERCENT].Float;
        }

        public static void SetSelfTimePercent(this sample_t self, float value)
        {
            self[SELF_TIME_PERCENT] = value;
        }

        public static float GetSelfTimePercent(this sample_t self)
        {
            return self[SELF_TIME_PERCENT].Float;
        }

        public static int GetNumCalls(this sample_t self)
        {
            return self[NUM_CALLS].Int;
        }

        public static void IncrementNumCalls(this sample_t self)
        {
            var numCalls = self.GetNumCalls();
            numCalls++;
            self[NUM_CALLS] = numCalls;
        }

        public static void CalculateTimes(this sample_t self, double rootTotalTime)
        {
            var startTimes = self.GetStartTimes();
            var endTimes = self.GetEndTimes();

            if (startTimes.Count == 0 || endTimes.Count == 0)
            {
                Debug.LogError($"no start/end times recorded for {self.GetName()}");
                return;
            }

            if (startTimes.Count != endTimes.Count)
            {
                Debug.LogError($"start times count for {self.GetName()} does not match end times count:" +
                    $"{startTimes.Count} != {endTimes.Count}");
                return;
            }

            double totalTime = endTimes[endTimes.Count - 1].Double - startTimes[0].Double;
            if (totalTime < 0)
            {
                Debug.LogError($"total time for {self.GetName()} is negative ({totalTime})");
                return;
            }
            self.SetTotalTimeMs(totalTime);

            double selfTime = 0;
            for (int i = 0; i < startTimes.Count; i++)
            {
                double startTime = startTimes[i].Double;
                double endTime = endTimes[i].Double;
                double deltaTime = endTime - startTime;
                if (deltaTime < 0)
                {
                    Debug.LogError($"delta time for {self.GetName()} at index {i} is negative ({deltaTime})");
                    return;
                }
                selfTime += deltaTime;
            }
            self.SetSelfTimeMs(selfTime);

            if (rootTotalTime == 0)
            {
                rootTotalTime = self.GetTotalTimeMs();
            }

            float totalTimePercent = (float)(totalTime / rootTotalTime) * 100f;
            self.SetTotalTimePercent(totalTimePercent);

            float selfTimePercent = (float)(selfTime / rootTotalTime) * 100f;
            self.SetSelfTimePercent(selfTimePercent);
        }

        public static string Encode(this sample_t self)
        {
            string str = "";

            str += self.GetPathName();
            str += ";";
            str += self.GetParent().GetPathName();
            str += ";";
            str += self.GetTotalTimePercent().ToString("F2");
            str += ";";
            str += self.GetSelfTimePercent().ToString("F2");
            str += ";";
            str += self.GetNumCalls();
            str += ";";
            str += (self.GetTotalTimeMs()).ToString("F4");
            str += ";";
            str += (self.GetSelfTimeMs()).ToString("F4");
            str += ";";

            DataList startTimes = self.GetStartTimes();
            for (int i = 0; i < startTimes.Count; i++)
            {
                str += (startTimes[i].Double).ToString("F4");
                if (i < startTimes.Count - 1)
                {
                    str += ",";
                }
            }
            str += ";";

            DataList endTimes = self.GetEndTimes();
            for (int i = 0; i < endTimes.Count; i++)
            {
                str += (endTimes[i].Double).ToString("F4");
                if (i < endTimes.Count - 1)
                {
                    str += ",";
                }
            }
            str += "\n";

            return str;
        }
    }
}

