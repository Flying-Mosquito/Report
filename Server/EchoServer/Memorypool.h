#pragma once

//template<class T,int ALLOC_BLOCK_SIZE=50>
//
//class Memorypool
//{
//public:
//	static VOID* operator new(std::size_t allocLength)
//		//new�� ���� ��� ȣ�� �˴ϴ�.
//	{
//		assert(sizeof(T) == allocLength)
//		assert(sizeof(T) >= sizeof(UCHAR*));
//
//		//���� �� �̻� �Ҵ��� �� ���� ������ ���� ���
//		if (!mFreePointer)
//			allocBlock();
//		UCHAR *ReturnPointer = mFreePointer;
//		mFreePointer = *reinterpret_cast<UCHAR**>(ReturnPointer);
//		//mFreePointer���� �����ϴ� ��� �տ� 4����Ʈ�� �ִ� �ּҰ� ���ϴ�.
//		return ReturnPointer;
//	}
//	
//	static VOID operator(VOID* deletePointer) //delete�� ������
//	{
//		*reinterpret_cast<UCHAR**>(deletePointer) = mFreePointer;
//		//delete�� ����� Next�� ���� mFreePointer�� �ּҸ� �־��ش�.
//		mFreePointer = static_cast<UCHAR*>(deletePointer);
//	}
//
//	Memorypool();
//	~Memorypool();
//};

