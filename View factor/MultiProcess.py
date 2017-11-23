import multiprocessing
import time

import ReadObj_
import ViewFactor

def run(all_faces, num_processes, start=0, end=None):
    if (end == None):
        end = len(all_faces)

    start_time = time.perf_counter()
    
    processes = list()
    recievers = list()
    to_do = end-start
    step = int(to_do/num_processes)

    for i in range(num_processes):
        start_index = i * step
        end_index = (i+1) * step if i < num_processes-1 else to_do

        recieving, sending = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=ViewFactor.run_everything, args=(all_faces, start_index, end_index, 5, sending))
        p.start()
        processes.append(p)
        recievers.append(recieving)

    # Wait for result
    result = list()
    for reciever in recievers:
        from_process = reciever.recv()
        result.extend(from_process)

    # Just to be sure
    for p in processes:
        p.join()

    ViewFactor.Export(result, time=time.perf_counter()-start_time)


if __name__ == "__main__":
    ReadObj_.GetAllInfo()
    run(ReadObj_.GetAllFaces(), multiprocessing.cpu_count())
