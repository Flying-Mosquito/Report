#pragma once

//template<class T,int ALLOC_BLOCK_SIZE=50>
//
//class Memorypool
//{
//public:
//	static VOID* operator new(std::size_t allocLength)
//		//new를 했을 경우 호출 됩니다.
//	{
//		assert(sizeof(T) == allocLength)
//		assert(sizeof(T) >= sizeof(UCHAR*));
//
//		//만약 더 이상 할당할 수 없는 공간이 없을 경우
//		if (!mFreePointer)
//			allocBlock();
//		UCHAR *ReturnPointer = mFreePointer;
//		mFreePointer = *reinterpret_cast<UCHAR**>(ReturnPointer);
//		//mFreePointer에는 리턴하는 블록 앞에 4바이트로 있던 주소가 들어갑니다.
//		return ReturnPointer;
//	}
//	
//	static VOID operator(VOID* deletePointer) //delete를 했을때
//	{
//		*reinterpret_cast<UCHAR**>(deletePointer) = mFreePointer;
//		//delete된 블록의 Next에 현재 mFreePointer의 주소를 넣어준다.
//		mFreePointer = static_cast<UCHAR*>(deletePointer);
//	}
//
//	Memorypool();
//	~Memorypool();
//};

