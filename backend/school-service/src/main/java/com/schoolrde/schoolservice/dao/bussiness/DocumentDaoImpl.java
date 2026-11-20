package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.dao.repository.DocumentRepository;
import com.schoolrde.schoolservice.entity.DocumentEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class DocumentDaoImpl implements DocumentDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(DocumentDaoImpl.class);

    private final DocumentRepository documentRepository;

    public DocumentDaoImpl(DocumentRepository documentRepository){
        this.documentRepository=documentRepository;
    }

    @Override
    public List<DocumentEntity> findDocumentByObjectIdAndObjectCategoryId(Integer objectId, Integer objectCategoryId){
        LOGGER.info("Quering document from database with objectId : {} and objectCategoryId : {}", objectId, objectCategoryId);
        return documentRepository.findByObjectIdAndObjectCategoryId(objectId, objectCategoryId);
    }

    @Override
    public List<DocumentEntity> findDocumentBySourceId(Integer sourceId){
        LOGGER.info("Quering document from database with sourceId : {}", sourceId);
        return documentRepository.findBySourceId(sourceId);
    }

    @Override
    public Optional<DocumentEntity> findDocumentById(Integer id){
        LOGGER.info("Quering document from database with id : {}", id);
        return documentRepository.findById(id);
    }

    @Override
    public DocumentEntity saveDocument(DocumentEntity documentEntity){
        LOGGER.info("document to be saved into DB : {}", JsonUtility.toJson(documentEntity));
        DocumentEntity savedDocumentEntity=documentRepository.save(documentEntity);
        LOGGER.info("document saved successfully : {}", JsonUtility.toJson(savedDocumentEntity));
        return savedDocumentEntity;
    }
}
