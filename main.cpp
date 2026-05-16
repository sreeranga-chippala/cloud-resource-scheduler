// Cloud Resource Reservation

#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <queue>
#include <iomanip>
#include <climits>

using namespace std;

const int MAX_WAIT = 50;

const int MAX_RETRIES = 20;


// EACH JOB

struct Job {

    int id;

    int cpu;
    int ram;
    int storage;
    int bw;

    int revenue;

    int arrival;
    int duration;
    int priority;

    int waitTime = 0;

    int retries = 0;

    double baseScore = 0.0;

    double score = 0.0;
};

// RESULT JOBS
struct Result {

    int accepted;
    int rejected;

    long long revenue;

    double cpuUtil;
    double ramUtil;
    double storageUtil;
    double bwUtil;
};

// RUNNING EVENT

struct Run {

    int endTime;

    Job job;
};

// INPUT
vector<Job> readInput(

    string file,

    int &maxCPU,
    int &maxRAM,
    int &maxStorage,
    int &maxBW
) {

    ifstream f(file);

    if (!f.is_open()) {

        cerr << "Input file error\n";

        exit(1);
    }

    f >> maxCPU
      >> maxRAM
      >> maxStorage
      >> maxBW;

    int n;

    f >> n;

    vector<Job> jobs(n);

    for (int i = 0; i < n; i++) {

        f >> jobs[i].cpu
          >> jobs[i].ram
          >> jobs[i].storage
          >> jobs[i].bw
          >> jobs[i].revenue
          >> jobs[i].arrival
          >> jobs[i].duration
          >> jobs[i].priority;

        jobs[i].id = i;
    }

    return jobs;
}

// PRIORITY SCORE

double computePriority(

    const Job &j,

    int maxCPU,
    int maxRAM,
    int maxStorage,
    int maxBW
) {

    double resourceCost =

        (double)j.cpu / maxCPU +

        (double)j.ram / maxRAM +

        (double)j.storage / maxStorage +

        (double)j.bw / maxBW;

    if (resourceCost < 1e-9)
        resourceCost = 1e-9;

    // Revenue per resource-time

    return

        (double)(
            j.revenue *
            j.priority
        )

        /

        (
            resourceCost *
            j.duration
        );
}

// STATIC GREEDY 

Result greedy(

    vector<Job> jobs,

    int maxCPU,
    int maxRAM,
    int maxStorage,
    int maxBW
) {

    for (auto &j : jobs) {

        j.baseScore =

            computePriority(
                j,
                maxCPU,
                maxRAM,
                maxStorage,
                maxBW
            );

        j.score = j.baseScore;
    }

    sort(

        jobs.begin(),
        jobs.end(),

        [](const Job &a,
           const Job &b) {

            return a.score >
                   b.score;
        }
    );

    int usedCPU = 0;
    int usedRAM = 0;
    int usedStorage = 0;
    int usedBW = 0;

    int accepted = 0;

    long long revenue = 0;

    for (auto &j : jobs) {

        bool fits =

            usedCPU + j.cpu <= maxCPU &&

            usedRAM + j.ram <= maxRAM &&

            usedStorage + j.storage <= maxStorage &&

            usedBW + j.bw <= maxBW;

        if (fits) {

            usedCPU += j.cpu;

            usedRAM += j.ram;

            usedStorage += j.storage;

            usedBW += j.bw;

            accepted++;

            revenue += j.revenue;
        }
    }

    return {

        accepted,

        (int)jobs.size() - accepted,

        revenue,

        100.0 * usedCPU / maxCPU,

        100.0 * usedRAM / maxRAM,

        100.0 * usedStorage / maxStorage,

        100.0 * usedBW / maxBW
    };
}

// ONLINE DISCRETE EVENT SCHEDULER

Result online(

    vector<Job> jobs,

    int maxCPU,
    int maxRAM,
    int maxStorage,
    int maxBW
) {
    ofstream logFile("outputs/logs/scheduler.log");

    ofstream timeline("outputs/metrics/timeline.csv");
    timeline
        << "Time,CPU,RAM,Storage,BW,Revenue,Queue\n";
    // INITIAL PRIORITY

    for (auto &j : jobs) {

        j.baseScore =

            computePriority(
                j,
                maxCPU,
                maxRAM,
                maxStorage,
                maxBW
            );

        j.score = j.baseScore;
    }

    // SORT ARRIVALS

    sort(

        jobs.begin(),
        jobs.end(),

        [](const Job &a,
           const Job &b) {

            return a.arrival <
                   b.arrival;
        }
    );

    // WAITING QUEUE

    auto cmpWaiting =

        [](const Job &a,
           const Job &b) {

            return a.score <
                   b.score;
        };

    priority_queue<
        Job,
        vector<Job>,
        decltype(cmpWaiting)
    > waiting(cmpWaiting);

    // RUNNING JOBS

    auto cmpRunning =

        [](const Run &a,
           const Run &b) {

            return a.endTime >
                   b.endTime;
        };

    priority_queue<
        Run,
        vector<Run>,
        decltype(cmpRunning)
    > running(cmpRunning);

    // RESOURCE TRACKING

    int usedCPU = 0;
    int usedRAM = 0;
    int usedStorage = 0;
    int usedBW = 0;

    int accepted = 0;

    int rejected = 0;

    long long revenue = 0;

    long long cpuTime = 0;
    long long ramTime = 0;
    long long storageTime = 0;
    long long bwTime = 0;

    int currentTime = 0;

// a -> 5cpu comes first - maxCpu = 10 ;  5->a arrival = 1 remCpu = 5
// b-> 6cpu comes after 'a' b-> waiting arrival = 3, b = 2*(1+...+20 priorites) -> reject
//c -> 5cpu comes after 'b' , a->5 and c -> 5 remCpu = 0, 
// 'a' completes remCpu = 5, c->5, d ->4cpu then d ->4 then remCpu = 1, 

    int idx = 0;

    // EVENT LOOP

    while (

        idx < jobs.size() ||

        !waiting.empty() ||

        !running.empty()
    ) {

        // NEXT EVENTS

        int nextArrival =

            (idx < jobs.size())

            ? jobs[idx].arrival

            : INT_MAX;

        int nextCompletion =

            (!running.empty())

            ? running.top().endTime

            : INT_MAX;

        int nextTime =

            min(
                nextArrival,
                nextCompletion
            );

        if (nextTime == INT_MAX)
            break;

        // UTILIZATION ACCOUNTING

        int delta =
            nextTime -
            currentTime;

        cpuTime +=
            1LL * usedCPU * delta;

        ramTime +=
            1LL * usedRAM * delta;

        storageTime +=
            1LL * usedStorage * delta;

        bwTime +=
            1LL * usedBW * delta;

        currentTime =
            nextTime;
        timeline
            << currentTime << ","
            << usedCPU << ","
            << usedRAM << ","
            << usedStorage << ","
            << usedBW << ","
            << revenue << ","
            << waiting.size()
            << "\n";
        // PROCESS COMPLETIONS

        while (

            !running.empty() &&

            running.top().endTime
            <= currentTime
        ) {

            Run r =
                running.top();

            running.pop();

            usedCPU -=
                r.job.cpu;

            usedRAM -=
                r.job.ram;

            usedStorage -=
                r.job.storage;

            usedBW -=
                r.job.bw;

            revenue +=
                r.job.revenue;
            logFile
                << "[TIME "
                << currentTime
                << "] JOB "
                << r.job.id
                << " COMPLETED\n";
        }

        // PROCESS ARRIVALS

        while (

            idx < jobs.size() &&

            jobs[idx].arrival
            <= currentTime
        ) {

            waiting.push(
                jobs[idx]
            );

            logFile
                << "[TIME "
                << currentTime
                << "] JOB "
                << jobs[idx].id
                << " ARRIVED\n";

            idx++;
        }

        // AGING REBUILD

        vector<Job> rebuilt;

        while (!waiting.empty()) {

            Job j =
                waiting.top();

            waiting.pop();

            j.waitTime++;

            j.retries++;

            double aging =

                1.0 +

                min(
                    0.5,
                    j.waitTime * 0.02
                );

            // FIXED LINEAR AGING

            j.score =
                j.baseScore * aging;

            rebuilt.push_back(j);
        }

        for (auto &j : rebuilt) {

            waiting.push(j);
        }

        // SCHEDULING

        vector<Job> skipped;

        while (!waiting.empty()) {

            Job j =
                waiting.top();

            waiting.pop();

            // REJECTION RULES

            bool reject =

                j.waitTime >
                MAX_WAIT ||

                j.retries >
                MAX_RETRIES;

            if (reject) {

                rejected++;
                logFile
                    << "[TIME "
                    << currentTime
                    << "] JOB "
                    << j.id
                    << " REJECTED\n";

                continue;
            }

            // RESOURCE FIT

            bool fits =

                usedCPU + j.cpu <= maxCPU &&

                usedRAM + j.ram <= maxRAM &&

                usedStorage + j.storage <= maxStorage &&

                usedBW + j.bw <= maxBW;

            // ACCEPT

            if (fits) {

                usedCPU +=
                    j.cpu;

                usedRAM +=
                    j.ram;

                usedStorage +=
                    j.storage;

                usedBW +=
                    j.bw;

                running.push({

                    currentTime +
                    j.duration,

                    j
                });

                accepted++;
                logFile
                    << "[TIME "
                    << currentTime
                    << "] JOB "
                    << j.id
                    << " ACCEPTED\n";
            }

            // RETRY LATER

            else {

                skipped.push_back(j);
            }
        }

        // REINSERT SKIPPED

        for (auto &j : skipped) {

            waiting.push(j);
        }
    }

    int totalTime =
        max(1, currentTime);

    logFile.close();
    timeline.close();

    return {

        accepted,

        rejected,

        revenue,

        100.0 *
        cpuTime /
        (1LL * totalTime * maxCPU),

        100.0 *
        ramTime /
        (1LL * totalTime * maxRAM),

        100.0 *
        storageTime /
        (1LL * totalTime * maxStorage),

        100.0 *
        bwTime /
        (1LL * totalTime * maxBW)
    };
}

void print(

    ofstream &out,

    string name,

    Result r
) {

    out << "\n=== "
        << name
        << " ===\n";

    out << "Accepted: "
        << r.accepted
        << endl;

    out << "Rejected: "
        << r.rejected
        << endl;

    out << "Revenue: "
        << "$" 
        << r.revenue
        << endl;

    out << fixed
        << setprecision(2);

    out << "--- Utilization ---\n";

    out << "CPU: "
        << r.cpuUtil
        << "%\n";

    out << "RAM: "
        << r.ramUtil
        << "%\n";

    out << "Storage: "
        << r.storageUtil
        << "%\n";

    out << "Bandwidth: "
        << r.bwUtil
        << "%\n";
}

int main() {

    int maxCPU;
    int maxRAM;
    int maxStorage;
    int maxBW;

    vector<Job> jobs =

        readInput(

            "builds/input.txt",

            maxCPU,
            maxRAM,
            maxStorage,
            maxBW
        );

    Result g =

        greedy(

            jobs,

            maxCPU,
            maxRAM,
            maxStorage,
            maxBW
        );

    Result o =

        online(

            jobs,

            maxCPU,
            maxRAM,
            maxStorage,
            maxBW
        );

    ofstream out("outputs/logs/output.txt");

    if (!out.is_open()) {

        cerr << "Output file error\n";

        return 1;
    }

    print(
        out,
        "Static Greedy Packing",
        g
    );

    print(
        out,
        "Online Discrete Event Scheduler",
        o
    );

    out << "\n=== Comparison ===\n";

    out << "Revenue Improvement: "
        << "$" 
        << o.revenue - g.revenue
        << endl;

    out << "Accepted Improvement: "
        << o.accepted - g.accepted
        << endl;

    out.close();

    ofstream metrics("outputs/metrics/metrics.csv");

    metrics << "Algorithm,Accepted,Rejected,Revenue,CPU,RAM,Storage,BW\n";

    metrics << "Greedy,"
            << g.accepted << ","
            << g.rejected << ","
            << g.revenue << ","
            << g.cpuUtil << ","
            << g.ramUtil << ","
            << g.storageUtil << ","
            << g.bwUtil << "\n";

    metrics << "Online,"
            << o.accepted << ","
            << o.rejected << ","
            << o.revenue << ","
            << o.cpuUtil << ","
            << o.ramUtil << ","
            << o.storageUtil << ","
            << o.bwUtil << "\n";

    metrics.close();

    return 0;
}