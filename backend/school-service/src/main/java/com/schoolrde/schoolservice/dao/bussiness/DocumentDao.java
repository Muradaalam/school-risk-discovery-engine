package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.DocumentEntity;

public interface DocumentDao{
	
    DocumentEntity saveDocument(DocumentEntity document);

    List<DocumentEntity> findDocumentByObjectIdAndObjectCategoryId(Integer objectId, Integer objectCategoryId);

    List<DocumentEntity> findDocumentBySourceId(Integer sourceId);

    Optional<DocumentEntity> findDocumentById(Integer id);

}
