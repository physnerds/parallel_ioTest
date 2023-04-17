/// \file
/// \Example macro to use TMPIFile.cxx
/// \This macro shows the usage of TMPIFile to simulate event reconstruction
///  and merging them in parallel
/// \To run this macro, once compiled, execute "mpirun -np <number of processors> ./bin/test_tmpi"
/// \macro_code
/// \Author Amit Bashyal


#include "TMPIFile.h"
#include "TFile.h"
#include "TROOT.h"
#include "TRandom.h"
#include "TTree.h"
#include "TSystem.h"
#include "TMemFile.h"
#include "TH1D.h"
#include <chrono>
#include <thread>
#include <ctime>

#include <iostream>

void test_tmpi(int n_collectors){
  char mpifname[100];
  clock_t t0,t1;  
 Int_t N_collectors= n_collectors; //specify how many collectors to receive the message
 Int_t sync_rate = 1000; //events per send request by the worker
 Int_t events_per_rank = 100000;
 Int_t sleep_mean = 5;
 Int_t sleep_sigma = 2;
  sprintf(mpifname,"Simple_MPIFile.root");
  TMPIFile *newfile = new TMPIFile("Simple_MPIFile.root","RECREATE",N_collectors);
  
  Int_t seed = newfile->GetMPILocalSize()+newfile->GetMPIColor()+newfile->GetMPILocalRank();

 //now we need to divide the collector and worker load from here..
 if(newfile->IsCollector())newfile->RunCollector(); //Start the Collector Function
 else{ //Workers' part
TTree *tree = new TTree("tree","tree");
 tree->SetAutoFlush(400000000);
 Float_t px,py;
 Int_t reco_time;
 tree->Branch("px",&px);
// tree->Branch("py",&py);
// tree->Branch("reco_time",&reco_time);
 gRandom->SetSeed(seed);
  Int_t   sleep=0;
  auto sync_start = std::chrono::high_resolution_clock::now();

 //total number of entries

 t0 = clock();
   for(int i=0;i<events_per_rank;i++){
     //    std::cout<<"Event "<<i<<" local rank "<<newfile->GetMPILocalRank()<<std::endl;
     gRandom->Rannor(px,py);
     sleep = abs(gRandom->Gaus(sleep_mean,sleep_sigma));
     //sleep after every events to simulate the reconstruction time... 
  //   std::this_thread::sleep_for(std::chrono::seconds(sleep));
     reco_time=sleep;
     tree->Fill();
      //at the end of the event loop...put the sync function
      //************START OF SYNCING IMPLEMENTATION FROM USERS' SIDE**********************
     if((i+1)%sync_rate==0){
	    newfile->Sync(); //this one as a worker...
	    tree->Reset();
         auto end = std::chrono::high_resolution_clock::now();
         double sync_time = std::chrono::duration_cast<std::chrono::duration<double>>(end - sync_start).count();
     //       printf("Rank", "[%d] [%d]\tevent collection time: %f", newfile->GetMPIColor(), newfile->GetMPILocalRank(),
          //       sync_time);         
	      }

   }
   //do the syncing one more time
   if(events_per_rank%sync_rate!=0)newfile->Sync(); 
   //************END OF SYNCING IMPLEMENTATION FROM USERS' SIDE***********************
 }
//   printf("Rank", "[%d] [%d]\tclosing file", newfile->GetMPIColor(), newfile->GetMPILocalRank()); 
  t1 = clock();
  auto t1sum = ((double)(t1-t0))/CLOCKS_PER_SEC;    
  std::cout<<"Time Taken for Execution "<<t1sum<<" RANK "<<newfile->GetMPILocalRank()<<std::endl;
 newfile->Close();
 
}

int main(int argc,char* argv[]){
  int rank,size;
  MPI_Init(&argc,&argv);
  MPI_Comm_rank(MPI_COMM_WORLD,&rank);
  MPI_Comm_size(MPI_COMM_WORLD,&size);
  int n_collectors = 1;
  if(argc>1) n_collectors = atoi(argv[1]);
  if(size<n_collectors){
   std::cout<<"Total number of Ranks should be greater than or equal to number of Collectors "<<
       size<<" "<<n_collectors<<std::endl;
   exit(1);
  }
  test_tmpi( n_collectors);
  Int_t finalized = 0;
  MPI_Finalized(&finalized);
  if(!finalized)  
    MPI_Finalize();
  return 0;
}

